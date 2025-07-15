from fastapi import APIRouter, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase
from ..models import Role  # reuse or define a Student model

router = APIRouter(prefix="/teacher/students", tags=["teacher-students"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/", response_model=List[dict])
def list_students(filter: str = Query("all"), token: str = Depends(oauth2)):
    # TODO: Query supabase for students, apply filters (need help, health alerts, top performers)
    return [
        {"id": "es_001", "name": "Emma Smith", "status": "health-alert", "grade": "A", "tasks": 95},
        # ... more students
    ]