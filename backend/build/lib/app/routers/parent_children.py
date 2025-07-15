from fastapi import APIRouter, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from ..config import supabase

router = APIRouter(prefix="/parent/children", tags=["parent-children"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/", response_model=List[dict])
def list_children(filter: Optional[str] = Query(None), token: str = Depends(oauth2)):
    """List all children under this parent, optionally filtering by name."""
    # TODO: fetch from supabase
    return [
        {"id": "john_jr", "name": "John Smith Jr.", "status": "ok"},
        # ... more children
    ]