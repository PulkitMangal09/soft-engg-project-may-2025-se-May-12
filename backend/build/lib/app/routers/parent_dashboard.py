from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase

router = APIRouter(prefix="/parent/dashboard", tags=["parent-dashboard"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/")
def get_parent_dashboard(token: str = Depends(oauth2)):
    """Return overview cards for parent dashboard (children count, requests, active tasks)."""
    return {
        "childrenCount": 3,
        "pendingRequests": 2,
        "activeTasks": 15,
        "children": ["john_jr","emma","sophie"],
        "alerts": [
            {"type": "health", "message": "Emma's blood sugar elevated (180 mg/dL)"},
            # ... more alerts
        ]
    }