from fastapi import APIRouter, Path, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase

router = APIRouter(prefix="/teacher/reports", tags=["teacher-reports"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/{student_id}")
def student_report(student_id: str = Path(...), token: str = Depends(oauth2)):
    # TODO: Query supabase for student profile, health summary, academic performance, recent activity
    return {
        "id": student_id,
        "name": "Emma Smith",
        "status": "Critical: High blood sugar",
        "overallGrade": "A",
        "completion": "95%",
        "tasksDone": 27,
        "healthSummary": {...},
        "academicPerformance": {...},
        "recentActivity": [...]  
    }