from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any
from ..config import supabase

router = APIRouter(prefix="/student/tasks", tags=["student-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_user_id(token: str) -> str:
    auth_res = supabase.auth.get_user(token)
    if getattr(auth_res, 'error', None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth_res.user.id

@router.get("/", response_model=List[Dict[str, Any]])
def list_tasks(token: str = Depends(oauth2)):
    """List all tasks assigned to the authenticated student."""
    user_id = get_user_id(token)
    resp = supabase.table("tasks").select("*").eq("assigned_to", user_id).execute()
    data = getattr(resp, 'data', None) or []
    return data

@router.get("/{task_id}", response_model=Dict[str, Any])
def get_task(task_id: str, token: str = Depends(oauth2)):
    """Retrieve a specific task by ID for the authenticated student."""
    user_id = get_user_id(token)
    resp = supabase.table("tasks").select("*").eq("task_id", task_id).eq("assigned_to", user_id).single().execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="Task not found")
    return data

@router.post("/", response_model=Dict[str, Any])
def add_task(task: Dict[str, Any], token: str = Depends(oauth2)):
    """Add a new task for the authenticated student."""
    user_id = get_user_id(token)
    task_data: Dict[str, Any] = {
        "title": task.get("title"),
        "description": task.get("description"),
        "assigned_to": user_id,
        "assigned_by": user_id,
        "category": task.get("category"),
        "priority": task.get("priority", "medium"),
        "due_date": task.get("due_date"),
        "due_time": task.get("due_time"),
        "status": task.get("status", "pending"),
    }
    if task.get("reward_points") is not None:
        task_data["reward_points"] = task["reward_points"]
    if task.get("attachment_url"):
        task_data["attachment_url"] = task["attachment_url"]

    resp = supabase.table("tasks").insert(task_data).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]

@router.patch("/{task_id}", response_model=Dict[str, Any])
def update_task(task_id: str, task: Dict[str, Any], token: str = Depends(oauth2)):
    """Update an existing task if it's not completed."""
    user_id = get_user_id(token)
    # Fetch current status
    current = supabase.table("tasks").select("status").eq("task_id", task_id).eq("assigned_to", user_id).single().execute().data
    if not current:
        raise HTTPException(status_code=404, detail="Task not found")
    if current.get("status") == "completed":
        raise HTTPException(status_code=400, detail="Cannot edit a completed task")
    resp = supabase.table("tasks").update(task).eq("task_id", task_id).eq("assigned_to", user_id).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]

@router.delete("/{task_id}", response_model=Dict[str, Any])
def delete_task(task_id: str, token: str = Depends(oauth2)):
    """Delete a task by ID for the authenticated student."""
    user_id = get_user_id(token)
    resp = supabase.table("tasks").delete().eq("task_id", task_id).eq("assigned_to", user_id).execute()
    # data list may be empty on deletion
    return {"deleted": True}