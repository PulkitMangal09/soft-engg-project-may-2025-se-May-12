from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase

router = APIRouter(prefix="/student/tasks", tags=["student-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/", response_model=List[dict])
def list_tasks(token: str = Depends(oauth2)):
    """List all tasks assigned to the student."""
    # TODO: fetch from supabase
    return []

@router.post("/", response_model=dict)
def add_task(task: dict, token: str = Depends(oauth2)):
    """Add a new task for the student."""
    # TODO: insert into supabase
    return task