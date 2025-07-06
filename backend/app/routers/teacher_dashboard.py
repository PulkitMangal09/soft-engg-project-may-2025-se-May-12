from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase

router = APIRouter(prefix="/teacher/dashboard", tags=["teacher-dashboard"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/")
def get_dashboard_summary(token: str = Depends(oauth2)):
    # TODO: Query supabase for class stats, health alerts, pending tasks, class average
    return {
        "class": {"grade": "9A", "subject": "Financial Literacy", "students": 28},
        "healthAlerts": {"urgent": 2},
        "pendingTasks": {"awaitingReview": 15},
        "classAverage": {"grade": "B+", "trend": "Improving"}
    }