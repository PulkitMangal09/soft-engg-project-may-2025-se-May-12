from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase

router = APIRouter(prefix="/student/dashboard", tags=["student-dashboard"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/")
def get_student_dashboard(token: str = Depends(oauth2)):
    """Return overview cards for student dashboard (tasks, finance, emotions, diet, health)."""
    return {
        "tasks": {"count": 0, "url": "/student/tasks"},
        "finance": {"balance": 0, "income": 0, "expenses": 0, "savings": 0, "url": "/student/finance"},
        "emotions": {"todayMood": null, "url": "/student/emotions"},
        "diet": {"calories": 0, "waterGlasses": 0, "url": "/student/diet"},
        "health": {"latestStats": {}, "url": "/student/health"}
    }