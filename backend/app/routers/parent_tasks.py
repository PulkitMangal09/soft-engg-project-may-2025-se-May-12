from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from ..config import supabase
from ..models import TaskCreate, TaskUpdate # Assuming these Pydantic models exist
from datetime import datetime, timezone

router = APIRouter(prefix="/parent/tasks", tags=["parent-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

# =============================================
# HELPER FUNCTION - CORE LOGIC
# =============================================

def get_parent_children_ids(parent_user_id: UUID) -> List[UUID]:
    """
    Resolve parent's children via family groups/members:
    - Families where the user is family_head_id OR a member with role in ("head", "parent") and is_active.
    - Children are members in those families with role = "child" and is_active.
    Returns list of child UUIDs.
    """
    # Families where user is head
    head_resp = (
        supabase.table("family_groups")
        .select("family_id")
        .eq("family_head_id", str(parent_user_id))
        .eq("is_active", True)
        .execute()
    )
    head_family_ids = {row.get("family_id") for row in (head_resp.data or [])}

    # Families where user is parent/head member
    member_resp = (
        supabase.table("family_members")
        .select("family_id, role, is_active")
        .eq("user_id", str(parent_user_id))
        .eq("is_active", True)
        .execute()
    )
    member_family_ids = {row.get("family_id") for row in (member_resp.data or []) if row.get("role") in ("head", "parent")}

    family_ids = list(head_family_ids.union(member_family_ids))
    if not family_ids:
        return []

    # Children within these families
    fm_resp = (
        supabase.table("family_members")
        .select("user_id, role, is_active")
        .in_("family_id", family_ids)
        .eq("role", "child")
        .eq("is_active", True)
        .execute()
    )
    child_ids: List[UUID] = []
    for row in (fm_resp.data or []):
        uid = row.get("user_id")
        if not uid:
            continue
        try:
            child_ids.append(UUID(uid))
        except Exception:
            # Skip malformed ids
            continue
    return child_ids

# =============================================
# PARENT TASK ENDPOINTS
# =============================================

@router.get("/summary")
def get_tasks_summary(token: str = Depends(oauth2)):
    # Step 1: Get current user and their children
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    child_ids_str = [str(cid) for cid in get_parent_children_ids(user.id)]
    if not child_ids_str:
        return {"activeTasks": 0, "overdue": 0, "completionRate": "0%", "totalThisMonth": 0}

    # Step 2: Fetch tasks assigned TO the parent's children
    tasks_resp = supabase.table("tasks").select("*").in_("assigned_to", child_ids_str).execute()
    tasks = tasks_resp.data or []

    # Step 3: Calculate metrics
    now = datetime.now(timezone.utc).isoformat()
    total_tasks = len(tasks)
    active_tasks = [t for t in tasks if t["status"] not in ("completed", "cancelled")]
    overdue_tasks = [t for t in active_tasks if t["due_date"] and t["due_date"] < now]

    completed_tasks = [t for t in tasks if t["status"] == "completed"]
    completion_rate = (len(completed_tasks) / total_tasks * 100) if total_tasks else 0

    current_month = datetime.now().month
    tasks_this_month = [
        t for t in tasks
        if t["created_at"] and datetime.fromisoformat(t["created_at"].replace('Z', '+00:00')).month == current_month
    ]

    return {
        "activeTasks": len(active_tasks),
        "overdue": len(overdue_tasks),
        "completionRate": f"{round(completion_rate)}%",
        "totalThisMonth": len(tasks_this_month)
    }

@router.get("/recent")
def recent_tasks(token: str = Depends(oauth2)):
    # Step 1: Get current user and their children
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    child_ids_str = [str(cid) for cid in get_parent_children_ids(user.id)]
    if not child_ids_str:
        return []

    # Step 2: Fetch recent tasks assigned to children
    task_resp = supabase.table("tasks") \
        .select("task_id, title, due_date, assigned_to, status") \
        .in_("assigned_to", child_ids_str) \
        .order("due_date", desc=True) \
        .limit(10) \
        .execute()
    tasks = task_resp.data or []

    # Step 3: Fetch names of the children for better context
    children_users_resp = supabase.table("users").select("user_id, full_name").in_("user_id", child_ids_str).execute()
    child_name_map = {user['user_id']: user['full_name'] for user in children_users_resp.data}

    # Step 4: Format the response
    result = []
    for task in tasks:
        completed_status = "1/1" if task["status"] == "completed" else "0/1"
        result.append({
            "title": task["title"],
            "due": task["due_date"],
            "assignedTo": child_name_map.get(task["assigned_to"], "Unknown Child"),
            "completed": completed_status
        })

    return result

@router.get("/overdue")
def overdue_tasks(token: str = Depends(oauth2)):
    # Step 1: Get current user and their children
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    child_ids_str = [str(cid) for cid in get_parent_children_ids(user.id)]
    if not child_ids_str:
        return []

    # Step 2: Fetch overdue tasks for these children
    now = datetime.now(timezone.utc).isoformat()
    task_resp = supabase.table("tasks") \
        .select("task_id, title, due_date, assigned_to") \
        .in_("assigned_to", child_ids_str) \
        .in_("status", ["pending", "in_progress"]) \
        .lt("due_date", now) \
        .order("due_date", desc=True) \
        .execute()
    tasks = task_resp.data or []

    # Step 3: Fetch child names for context
    children_users_resp = supabase.table("users").select("user_id, full_name").in_("user_id", child_ids_str).execute()
    child_name_map = {user['user_id']: user['full_name'] for user in children_users_resp.data}

    # Step 4: Format response
    result = []
    for task in tasks:
        result.append({
            "title": task["title"],
            "due": task["due_date"],
            "assignedTo": child_name_map.get(task["assigned_to"], "Unknown Child")
        })

    return result

# --- Create a Task (Secure) ---
@router.post("/", status_code=201)
def create_task(task: TaskCreate, token: str = Depends(oauth2)):
    # Step 1: Get current user and their children
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    child_ids = get_parent_children_ids(user.id)

    # Step 2: Authorization Check
    if task.assigned_to not in child_ids:
        raise HTTPException(status_code=403, detail="You are not authorized to assign tasks to this user.")

    # Step 3: Insert the task, ensuring assigned_by is the current parent
    task_data = task.dict()
    task_data['assigned_by'] = str(user.id)

    # Ensure JSON serializable payload (convert UUIDs and datetimes)
    from datetime import datetime, date
    serializable = {}
    for k, v in task_data.items():
        if isinstance(v, UUID):
            serializable[k] = str(v)
        elif isinstance(v, (datetime, date)):
            # ISO format; for date it yields YYYY-MM-DD
            serializable[k] = v.isoformat()
        else:
            serializable[k] = v

    try:
        response = supabase.table("tasks").insert(serializable).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create task: {e}")
    # Some clients return an APIResponse with .data; ensure we have a row
    data = getattr(response, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Failed to create task")
    return data[0]

# --- Read All Tasks for Parent's Children (Secure) ---
@router.get("/", response_model=List[dict])
def get_all_tasks(token: str = Depends(oauth2)):
    # Step 1: Get current user and their children
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    child_ids_str = [str(cid) for cid in get_parent_children_ids(user.id)]
    if not child_ids_str:
        return []

    # Step 2: Fetch only tasks assigned to the children
    response = supabase.table("tasks").select("*").in_("assigned_to", child_ids_str).order("created_at", desc=True).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

# --- Read Single Task by ID (Secure) ---
@router.get("/{task_id}", response_model=dict)
def get_task(task_id: UUID, token: str = Depends(oauth2)):
    # Step 1: Get current user and their children
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    child_ids = get_parent_children_ids(user.id)

    # Step 2: Fetch the task
    response = supabase.table("tasks").select("*").eq("task_id", str(task_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = response.data

    # Step 3: Authorization Check
    if UUID(task['assigned_to']) not in child_ids:
        raise HTTPException(status_code=404, detail="Task not found") # Use 404 to not leak info

    return task

# --- Update Task (Secure) ---
@router.put("/{task_id}")
def update_task(task_id: UUID, task_update: TaskUpdate, token: str = Depends(oauth2)):
    # Step 1: Get current user and their children
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    child_ids = get_parent_children_ids(user.id)

    # Step 2: Fetch the existing task to verify ownership
    existing_task_resp = supabase.table("tasks").select("assigned_to, assigned_by").eq("task_id", str(task_id)).single().execute()
    if not existing_task_resp.data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    existing_task = existing_task_resp.data

    # Step 3: Authorization Check (Must be assigned to their child AND assigned by them)
    if UUID(existing_task['assigned_to']) not in child_ids or UUID(existing_task['assigned_by']) != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to modify this task.")

    # Step 4: Perform the update
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    try:
        supabase.table("tasks").update(update_data).eq("task_id", str(task_id)).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update task: {e}")
    return {"message": "Task updated successfully"}

# --- Delete Task (Secure) ---
@router.delete("/{task_id}")
def delete_task(task_id: UUID, token: str = Depends(oauth2)):
    # Step 1: Get current user and their children
    auth_resp = supabase.auth.get_user(token)
    user = auth_resp.user
    if not user or not user.id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    child_ids = get_parent_children_ids(user.id)

    # Step 2: Fetch the existing task to verify ownership
    existing_task_resp = supabase.table("tasks").select("assigned_to, assigned_by").eq("task_id", str(task_id)).single().execute()
    if not existing_task_resp.data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    existing_task = existing_task_resp.data

    # Step 3: Authorization Check (Must be assigned to their child AND assigned by them)
    if UUID(existing_task['assigned_to']) not in child_ids or UUID(existing_task['assigned_by']) != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this task.")

    # Step 4: Perform the deletion
    try:
        supabase.table("tasks").delete().eq("task_id", str(task_id)).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete task: {e}")
    return {"message": "Task deleted successfully"}