from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from uuid import UUID
from ..config import supabase
from ..models import TaskBase, TaskCreate

router = APIRouter(prefix="/student/tasks", tags=["student-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_user_id(token: str) -> UUID:
    auth_res = supabase.auth.get_user(token)
    if getattr(auth_res, 'error', None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth_res.user.id

@router.get("/", response_model=List[TaskBase])
def list_tasks(token: str = Depends(oauth2)):
    """List all tasks assigned to the authenticated student."""
    user_id = get_user_id(token)
    resp = supabase.table("tasks").select("*").eq("assigned_to", user_id).execute()
    return resp.data or []

@router.get("/{task_id}", response_model=TaskBase)
def get_task(task_id: UUID, token: str = Depends(oauth2)):
    """Retrieve a specific task by ID for the authenticated student."""
    user_id = get_user_id(token)
    resp = supabase.table("tasks").select("*")\
        .eq("task_id", task_id).eq("assigned_to", user_id).single().execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return resp.data

@router.post("/", response_model=TaskBase)
def add_task(task: TaskCreate, token: str = Depends(oauth2)):
    """Add a new task for the authenticated student."""
    user_id = get_user_id(token)
    payload = task.dict()
    # Convert datetime/time fields to ISO strings
    if payload.get("due_date"):
        payload["due_date"] = payload["due_date"].isoformat()
    if payload.get("due_time"):
        payload["due_time"] = payload["due_time"].isoformat()
    payload.update({
        "assigned_to": user_id,
        "assigned_by": user_id,
    })
    resp = supabase.table("tasks").insert(payload).execute()
    data = resp.data
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    return data[0]

@router.patch("/{task_id}", response_model=TaskBase)
def update_task(task_id: UUID, task: TaskCreate, token: str = Depends(oauth2)):
    """Update an existing task if it's not completed."""
    user_id = get_user_id(token)
    current = supabase.table("tasks") \
        .select("status") \
        .eq("task_id", task_id) \
        .eq("assigned_to", user_id) \
        .single() \
        .execute().data
    if not current:
        raise HTTPException(status_code=404, detail="Task not found")
    if current.get("status") == "completed":
        raise HTTPException(status_code=400, detail="Cannot edit a completed task")

    # Prepare payload and convert datetimes to ISO strings
    payload = task.dict(exclude_unset=True)
    if payload.get("due_date"):
        payload["due_date"] = payload["due_date"].isoformat()
    if payload.get("due_time"):
        payload["due_time"] = payload["due_time"].isoformat()

    resp = supabase.table("tasks") \
        .update(payload) \
        .eq("task_id", task_id) \
        .eq("assigned_to", user_id) \
        .execute()
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]


@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: UUID, token: str = Depends(oauth2)):
    """Delete a task by ID for the authenticated student."""
    user_id = get_user_id(token)
    supabase.table("tasks").delete()\
        .eq("task_id", task_id).eq("assigned_to", user_id).execute()
    return {"deleted": True}