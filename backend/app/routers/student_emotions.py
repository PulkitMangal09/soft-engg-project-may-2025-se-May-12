from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase

router = APIRouter(prefix="/student/emotions", tags=["student-emotions"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/mood-trends")
def mood_trends(token: str = Depends(oauth2)):
    """Return recent mood trend data for charting."""
    return []

@router.post("/log", response_model=dict)
def log_emotion(entry: dict, token: str = Depends(oauth2)):
    """Log a new emotion check-in."""
    return entry