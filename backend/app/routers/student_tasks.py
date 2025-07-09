from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase

router = APIRouter(prefix="/student/tasks", tags=["student-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/", response_model=List[dict])
def list_tasks(token: str = Depends(oauth2)):
    """List all tasks assigned to the student."""
    # TODO: fetch from supabase table "tasks"
    resp = supabase.table("tasks").select("*").eq("assigned_to", supabase.auth.get_user(token).user.id).execute()
    if resp.error:
        raise HTTPException(status_code=500, detail=str(resp.error))
    return resp.data or []

@router.post("/", response_model=dict)
def add_task(task: dict, token: str = Depends(oauth2)):
    """Add a new task for the student."""
    # 1. Retrieve authenticated user ID
    user_res = supabase.auth.api.get_user(token)
    user_id = getattr(user_res, 'id', None) or user_res.get('id') if isinstance(user_res, dict) else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 2. Build task record
    task_data = {
        "title":         task.get("title"),
        "description":   task.get("description"),
        "assigned_to":   user_id,
        "assigned_by":   user_id,
        "category":      task.get("category"),
        "priority":      task.get("priority", "medium"),
        "due_date":      task.get("due_date"),
        "due_time":      task.get("due_time"),
        "status":        task.get("status", "pending")
    }

    # 3. Insert to Supabase
    db_res = supabase.table("tasks").insert(task_data).select("*").execute()
    if db_res.error:
        raise HTTPException(status_code=500, detail=str(db_res.error))

    # 4. Return created task
    created = db_res.data[0] if isinstance(db_res.data, list) else db_res.data
    return created