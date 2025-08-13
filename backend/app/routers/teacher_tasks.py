from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from pydantic import BaseModel, Field, EmailStr

from ..config import supabase
from ..models import TaskBase, TaskUpdate  # TaskBase has task_id, assigned_*; TaskUpdate = partial

router = APIRouter(prefix="/teacher/tasks", tags=["teacher-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_user_id(token: str) -> UUID:
    auth_res = supabase.auth.get_user(token)
    if getattr(auth_res, 'error', None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = auth_res.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user.id


# Accepts which student to assign to; teacher is assigned_by automatically
class TeacherTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    # Store time as "HH:MM" or "HH:MM:SS"; we will pass through strings safely
    due_time: Optional[str] = None
    status: Optional[str] = "pending"
    reward_points: Optional[int] = 0
    attachment_url: Optional[str] = None

    # target student (provide exactly one)
    assigned_to: Optional[UUID] = Field(None, description="Student user_id to assign the task to")
    assigned_to_email: Optional[EmailStr] = Field(None, description="Student email to assign the task to")


@router.get("/summary")
def get_tasks_summary(token: str = Depends(oauth2)):
    teacher_id = get_user_id(token)
    now_iso = datetime.now(timezone.utc).isoformat()

    # All tasks assigned_by this teacher
    tasks_resp = supabase.table("tasks").select("*").eq("assigned_by", teacher_id).execute()
    tasks = tasks_resp.data or []

    total = len(tasks)
    active = [t for t in tasks if t.get("status") not in ("completed", "cancelled")]
    # If due_date is stored as timestamp/ISO strings, comparing to now_iso via lt in SQL is better,
    # but this approximation works when values are ISO strings. We still try to parse safely:
    overdue = []
    for t in active:
        dd = t.get("due_date")
        if not dd:
            continue
        try:
            # Allow both ISO strings and naive strings
            dt = datetime.fromisoformat(dd.replace("Z", "+00:00")) if isinstance(dd, str) else dd
        except Exception:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if dt.isoformat() < now_iso:
            overdue.append(t)

    # Completion rate via task_completions
    # Normalize to strings for stable comparison in PostgREST filters
    task_ids = [str(t.get("task_id")) for t in tasks if t.get("task_id")]
    completed_count = 0
    if task_ids:
        completions_resp = (
            supabase.table("task_completions")
            .select("task_id")
            .in_("task_id", task_ids)
            .execute()
        )
        completions = getattr(completions_resp, "data", None) or []
        # Coerce to str and drop nulls to avoid falsy mismatches
        completed_task_ids = {str(c.get("task_id")) for c in completions if c.get("task_id")}

    # Also include tasks directly marked as completed in tasks table
    status_completed_ids = {str(t.get("task_id")) for t in tasks if str(t.get("status")) == "completed" and t.get("task_id")}
    completed_union = completed_task_ids.union(status_completed_ids) if task_ids else status_completed_ids
    completed_count = len(completed_union)

    completion_rate = round((completed_count / total * 100), 0) if total else 0

    # Created this month
    now = datetime.now(timezone.utc)
    this_month = now.month
    this_year = now.year

    def is_this_month(created_at):
        if not created_at:
            return False
        try:
            dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.month == this_month and dt.year == this_year
        except Exception:
            return False

    created_this_month = sum(1 for t in tasks if is_this_month(t.get("created_at")))

    return {
        "activeTasks": len(active),
        "overdue": len(overdue),
        "completionRate": f"{int(completion_rate)}%",
        "totalThisMonth": created_this_month,
    }


@router.get("/recent")
def recent_tasks(token: str = Depends(oauth2)):
    teacher_id = get_user_id(token)

    task_resp = (
        supabase.table("tasks")
        .select("task_id, title, due_date, status")
        .eq("assigned_by", teacher_id)
        .order("due_date", desc=True)
        .limit(10)
        .execute()
    )
    tasks = task_resp.data or []
    task_ids = [t["task_id"] for t in tasks if t.get("task_id")]

    completion_map = {}
    if task_ids:
        completions_resp = supabase.table("task_completions") \
            .select("task_id") \
            .in_("task_id", task_ids) \
            .execute()
        for c in (completions_resp.data or []):
            tid = c["task_id"]
            completion_map[tid] = completion_map.get(tid, 0) + 1

    # For now assume each task is assigned to exactly one student
    result = []
    for t in tasks:
        tid = t["task_id"]
        completed = completion_map.get(tid, 0)
        total = 1
        is_completed = bool(completed >= total) or (str(t.get("status")) == "completed")
        result.append({
            "title": t["title"],
            "due": t["due_date"],
            "status": t.get("status"),
            "is_completed": is_completed,
            "completed": f"{completed}/{total}",
        })
    return result


@router.get("/overdue")
def overdue_tasks(token: str = Depends(oauth2)):
    teacher_id = get_user_id(token)
    now_iso = datetime.now(timezone.utc).isoformat()

    task_resp = (
        supabase.table("tasks")
        .select("task_id, title, due_date")
        .eq("assigned_by", teacher_id)
        .in_("status", ["pending", "in_progress"])
        .lt("due_date", now_iso)
        .order("due_date", desc=True)
        .limit(10)
        .execute()
    )
    tasks = task_resp.data or []
    return [{"title": t["title"], "due": t["due_date"]} for t in tasks]


# --- Create a Task (teacher assigns) ---
@router.post("/", response_model=TaskBase, status_code=201)
def create_task(task: TeacherTaskCreate, token: str = Depends(oauth2)):
    teacher_id = get_user_id(token)
    payload = task.dict()

    # Validate assignment target: exactly one of assigned_to or assigned_to_email
    provided = int(bool(payload.get("assigned_to"))) + int(bool(payload.get("assigned_to_email")))
    if provided != 1:
        raise HTTPException(status_code=400, detail="Provide exactly one of assigned_to (UUID) or assigned_to_email (email)")

    # Resolve email to UUID if email path provided
    if payload.get("assigned_to_email"):
        email = payload["assigned_to_email"]
        user_rows = (
            supabase.table("users")
            .select("user_id, email, user_type")
            .eq("email", email)
            .eq("user_type", "student")
            .limit(1)
            .execute()
            .data
            or []
        )
        if not user_rows:
            raise HTTPException(status_code=400, detail="No student found with the provided email")
        payload["assigned_to"] = user_rows[0]["user_id"]
        # Remove helper field before insert
        payload.pop("assigned_to_email", None)

    # Ensure proper types & values
    if payload.get("due_date"):
        payload["due_date"] = payload["due_date"].isoformat()

    # Remove empty-string time to avoid Postgres time cast error
    if not payload.get("due_time"):
        payload.pop("due_time", None)

    payload["assigned_by"] = teacher_id

    resp = supabase.table("tasks").insert(payload).execute()
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]


# --- Read All Tasks (for this teacher) ---
@router.get("/", response_model=List[TaskBase])
def get_all_tasks(token: str = Depends(oauth2)):
    teacher_id = get_user_id(token)
    resp = (
        supabase.table("tasks")
        .select("*")
        .eq("assigned_by", teacher_id)
        .order("created_at", desc=True)
        .execute()
    )
    return resp.data or []


# --- Read Single Task by ID (must belong to this teacher) ---
@router.get("/{task_id}", response_model=TaskBase)
def get_task(task_id: UUID, token: str = Depends(oauth2)):
    teacher_id = get_user_id(token)
    resp = (
        supabase.table("tasks")
        .select("*")
        .eq("task_id", str(task_id))
        .eq("assigned_by", teacher_id)
        .single()
        .execute()
    )
    if getattr(resp, "error", None) or not resp.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return resp.data


# --- Update Task (partial) ---
@router.patch("/{task_id}", response_model=TaskBase)
def update_task(task_id: UUID, task: TaskUpdate, token: str = Depends(oauth2)):
    teacher_id = get_user_id(token)

    # Ensure it belongs to teacher
    current = (
        supabase.table("tasks")
        .select("status")
        .eq("task_id", str(task_id))
        .eq("assigned_by", teacher_id)
        .single()
        .execute()
        .data
    )
    if not current:
        raise HTTPException(status_code=404, detail="Task not found")

    payload = task.dict(exclude_unset=True)

    if "due_date" in payload and payload["due_date"] is not None:
        payload["due_date"] = payload["due_date"].isoformat()

    if "due_time" in payload and not payload["due_time"]:
        # Avoid empty string going to Postgres time column
        payload.pop("due_time", None)

    resp = (
        supabase.table("tasks")
        .update(payload)
        .eq("task_id", str(task_id))
        .eq("assigned_by", teacher_id)
        .execute()
    )
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]


# --- Delete Task ---
@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: UUID, token: str = Depends(oauth2)):
    teacher_id = get_user_id(token)
    supabase.table("tasks").delete().eq("task_id", str(task_id)).eq("assigned_by", teacher_id).execute()
    return {"deleted": True}
