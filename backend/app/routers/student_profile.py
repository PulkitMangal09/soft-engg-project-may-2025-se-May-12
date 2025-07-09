from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, Literal
from ..config import supabase

router = APIRouter(prefix="/student/profile", tags=["student-profile"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Pydantic model for updates
class StudentProfileUpdate(BaseModel):
    student_number: Optional[str]
    grade_level: Optional[str]
    school_name: Optional[str]
    emergency_contact_phone: Optional[str]
    can_exist_independently: Optional[bool]

@router.get("/", response_model=dict)
def get_profile(token: str = Depends(oauth2)):
    """Get the authenticated student's profile."""
    u = supabase.auth.api.get_user(token)
    user_id = getattr(u, 'id', None) or u.get('id') if isinstance(u, dict) else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    resp = supabase.table("students").select("*").eq("student_id", user_id).single().execute()
    if resp.error:
        raise HTTPException(status_code=404, detail="Profile not found")
    return resp.data

@router.post("/", response_model=dict)
def create_profile(data: StudentProfileUpdate, token: str = Depends(oauth2)):
    """Create initial student profile stub (if not existing)."""
    u = supabase.auth.api.get_user(token)
    user_id = getattr(u, 'id', None) or u.get('id') if isinstance(u, dict) else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    payload = {"student_id": user_id, **data.dict(exclude_unset=True)}
    resp = supabase.table("students").insert(payload).select("*").execute()
    if resp.error:
        raise HTTPException(status_code=400, detail=str(resp.error))
    return resp.data[0]

@router.patch("/", response_model=dict)
def update_profile(data: StudentProfileUpdate, token: str = Depends(oauth2)):
    """Update the authenticated student's profile."""
    u = supabase.auth.api.get_user(token)
    user_id = getattr(u, 'id', None) or u.get('id') if isinstance(u, dict) else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    resp = supabase.table("students").update(data.dict(exclude_unset=True)).eq("student_id", user_id).select("*").execute()
    if resp.error:
        raise HTTPException(status_code=400, detail=str(resp.error))
    return resp.data[0]

@router.delete("/", response_model=dict)
def delete_profile(token: str = Depends(oauth2)):
    """Delete the authenticated student's profile."""
    u = supabase.auth.api.get_user(token)
    user_id = getattr(u, 'id', None) or u.get('id') if isinstance(u, dict) else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    resp = supabase.table("students").delete().eq("student_id", user_id).execute()
    if resp.error:
        raise HTTPException(status_code=400, detail=str(resp.error))
    return {"deleted": True}