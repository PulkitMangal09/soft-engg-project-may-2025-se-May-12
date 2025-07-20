from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone
from ..config import supabase
from ..models import TaskCreate, TaskUpdate

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from ..config import supabase
from datetime import datetime

router = APIRouter(prefix="/teacher/tasks", tags=["teacher-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

# @router.get("/summary")
# def get_tasks_summary(token: str = Depends(oauth2)):
#     # TODO: Query supabase for active tasks, overdue count, completion rate, total this month
#     return {
#         "activeTasks": 15,
#         "overdue": 5,
#         "completionRate": "85%",
#         "totalThisMonth": 156
#     }
@router.get("/summary")
def get_tasks_summary(token: str = Depends(oauth2)):
    # Step 1: Get current user from Supabase Auth
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = user.id
    now = datetime.now(timezone.utc).isoformat()

    # Step 2: Fetch tasks assigned by this teacher
    tasks_resp = supabase.table("tasks").select("*").eq("assigned_by", user_id).execute()
    tasks = tasks_resp.data or []

    total_tasks = len(tasks)
    active_tasks = [t for t in tasks if t["status"] not in ("completed", "cancelled")]
    overdue_tasks = [t for t in active_tasks if t["due_date"] and t["due_date"] < now]

    # Step 3: Completion rate
    task_ids = [t["task_id"] for t in tasks]
    completions_resp = supabase.table("task_completions").select("task_id").in_("task_id", task_ids).execute()
    completions = completions_resp.data or []
    completed_task_ids = set(c["task_id"] for c in completions)
    completion_rate = (len(completed_task_ids) / total_tasks * 100) if total_tasks else 0

    # Step 4: Tasks created this month
    current_month = datetime.now().month
    tasks_this_month = [
        t for t in tasks
        if t["created_at"] and datetime.fromisoformat(t["created_at"]).month == current_month
    ]

    return {
        "activeTasks": len(active_tasks),
        "overdue": len(overdue_tasks),
        "completionRate": f"{round(completion_rate)}%",
        "totalThisMonth": len(tasks_this_month)
    }

# @router.get("/recent", response_model=List[dict])
# def recent_tasks(token: str = Depends(oauth2)):
#     # TODO: list recent task info
#     return [
#         {"title": "Budget Analysis Project", "due": "Tomorrow", "completed": "23/28"},
#         # ... more tasks
#     ]
@router.get("/recent")
def recent_tasks(token: str = Depends(oauth2)):
    # Get teacher's user ID
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = user.id

    # Fetch recent tasks assigned by the teacher (sorted by due_date desc)
    task_resp = supabase.table("tasks") \
        .select("task_id, title, due_date") \
        .eq("assigned_by", user_id) \
        .order("due_date", desc=True) \
        .limit(10) \
        .execute()

    tasks = task_resp.data or []
    task_ids = [t["task_id"] for t in tasks]

    # Get completions per task_id
    completions_resp = supabase.table("task_completions") \
        .select("task_id") \
        .in_("task_id", task_ids) \
        .execute()

    completions = completions_resp.data or []

    # Count completions per task
    completion_map = {}
    for c in completions:
        tid = c["task_id"]
        if tid not in completion_map:
            completion_map[tid] = 0
        completion_map[tid] += 1

    # Since each task is assigned to only one student now
    result = []
    for task in tasks:
        task_id = task["task_id"]
        completed = completion_map.get(task_id, 0)
        total = 1  # one per task for now
        result.append({
            "title": task["title"],
            "due": task["due_date"],
            "completed": f"{completed}/{total}"
        })

    return result
### OverDue Task
@router.get("/overdue")
def overdue_tasks(token: str = Depends(oauth2)):
    # Get the current teacher (user)
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = user.id
    now = datetime.now(timezone.utc).isoformat()

    # Fetch overdue tasks
    task_resp = supabase.table("tasks") \
        .select("task_id, title, due_date") \
        .eq("assigned_by", user_id) \
        .in_("status", ["pending", "in_progress"]) \
        .lt("due_date", now) \
        .order("due_date", desc=True) \
        .limit(10) \
        .execute()

    tasks = task_resp.data or []

    result = []
    for task in tasks:
        result.append({
            "title": task["title"],
            "due": task["due_date"]
        })

    return result

# --- Create a Task ---
@router.post("/", status_code=201)
def create_task(task: TaskCreate, token: str = Depends(oauth2)):
    response = supabase.table("tasks").insert(task.dict()).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]

# --- Read All Tasks ---
@router.get("/", response_model=List[dict])
def get_all_tasks(token: str = Depends(oauth2)):
    response = supabase.table("tasks").select("*").order("created_at", desc=True).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

# --- Read Single Task by ID ---
@router.get("/{task_id}", response_model=dict)
def get_task(task_id: UUID, token: str = Depends(oauth2)):
    response = supabase.table("tasks").select("*").eq("task_id", str(task_id)).single().execute()
    if response.error or not response.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return response.data

# --- Update Task ---
@router.put("/{task_id}")
def update_task(task_id: UUID, task: TaskUpdate, token: str = Depends(oauth2)):
    update_data = {k: v for k, v in task.dict().items() if v is not None}
    response = supabase.table("tasks").update(update_data).eq("task_id", str(task_id)).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Task updated successfully"}

# --- Delete Task ---
@router.delete("/{task_id}")
def delete_task(task_id: UUID, token: str = Depends(oauth2)):
    response = supabase.table("tasks").delete().eq("task_id", str(task_id)).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Task deleted successfully"}
