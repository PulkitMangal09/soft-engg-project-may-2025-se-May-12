from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase

router = APIRouter(prefix="/student/health", tags=["student-health"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/stats")
def get_health_stats(token: str = Depends(oauth2)):
    """Return the student's latest health metrics and analytics."""
    return {"bmi":0, "weight":0, "alerts": []}

@router.post("/log", response_model=dict)
def log_health(entry: dict, token: str = Depends(oauth2)):
    """Log a new health data point (e.g., weight, blood sugar)."""
    return entry