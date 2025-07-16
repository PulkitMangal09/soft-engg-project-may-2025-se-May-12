from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase

router = APIRouter(prefix="/student/diet", tags=["student-diet"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/dashboard")
def get_diet_dashboard(token: str = Depends(oauth2)):
    """Return diet stats: calories, water intake, nutrition alerts."""
    return {"calories":0, "water":0, "alerts": []}

@router.post("/log-food", response_model=dict)
def log_food(entry: dict, token: str = Depends(oauth2)):
    """Log a food entry."""
    return entry

@router.post("/log-water", response_model=dict)
def log_water(count: int, token: str = Depends(oauth2)):
    """Add water glass count."""
    return {"water": count}