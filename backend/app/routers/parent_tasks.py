from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/parent/tasks", tags=["parent-tasks"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/summary")
def tasks_summary(token: str = Depends(oauth2)):
    """Return total and breakdown of active tasks across children."""
    return {"totalPending":12, "healthAlerts":1, "topAchievements":3}