from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/parent/family", tags=["parent-family"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/overview")
def family_overview(token: str = Depends(oauth2)):
    """Return summary cards for tasks, finance, health across family."""
    return {
        "tasks": {"pending":12},
        "finance": {"goalsActive":2},
        "health": {"alerts":1},
        "requests": {"pending":2}
    }