from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase

router = APIRouter(prefix="/teacher/tasks", tags=["teacher-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/summary")
def get_tasks_summary(token: str = Depends(oauth2)):
    # TODO: Query supabase for active tasks, overdue count, completion rate, total this month
    return {
        "activeTasks": 15,
        "overdue": 5,
        "completionRate": "85%",
        "totalThisMonth": 156
    }

@router.get("/recent", response_model=List[dict])
def recent_tasks(token: str = Depends(oauth2)):
    # TODO: list recent task info
    return [
        {"title": "Budget Analysis Project", "due": "Tomorrow", "completed": "23/28"},
        # ... more tasks
    ]