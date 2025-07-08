from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..config import supabase

router = APIRouter(prefix="/parent/requests", tags=["parent-requests"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/", response_model=List[dict])
def list_requests(token: str = Depends(oauth2)):
    """Get pending join or access requests from children."""
    return [
        {"childId": "emma", "type": "join", "date": "2025-06-30"},
        # ...
    ]

@router.post("/{child_id}/approve")
def approve_request(child_id: str, token: str = Depends(oauth2)):
    """Approve a pending request for a given child."""
    # TODO: update supabase
    return {"status": "approved", "childId": child_id}