from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from ..config import supabase

router = APIRouter(prefix="/student/profile", tags=["student-profile"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

class StudentProfileUpdate(BaseModel):
    student_number: Optional[str]
    grade_level: Optional[str]
    school_name: Optional[str]
    emergency_contact_phone: Optional[str]
    can_exist_independently: Optional[bool]

def get_user_id(token: str):
    auth_res = supabase.auth.get_user(token)
    if getattr(auth_res, 'error', None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth_res.user.id

@router.get("/", response_model=dict)
def get_profile(token: str = Depends(oauth2)):
    """Get the authenticated student's profile."""
    user_id = get_user_id(token)
    resp = supabase.table("students").select("*").eq("student_id", user_id).single().execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return data

@router.post("/", response_model=dict)
def create_profile(data: StudentProfileUpdate, token: str = Depends(oauth2)):
    """Create initial student profile stub (if not existing)."""
    user_id = get_user_id(token)
    payload = {"student_id": user_id, **data.dict(exclude_unset=True)}
    resp = supabase.table("students").insert(payload).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Insert failed")
    # resp.data is a list
    return data[0]

@router.patch("/", response_model=dict)
def update_profile(data: StudentProfileUpdate, token: str = Depends(oauth2)):
    """Update the authenticated student's profile."""
    user_id = get_user_id(token)
    resp = supabase.table("students").update(data.dict(exclude_unset=True)).eq("student_id", user_id).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]

@router.delete("/", response_model=dict)
def delete_profile(token: str = Depends(oauth2)):
    """Delete the authenticated student's profile."""
    user_id = get_user_id(token)
    supabase.table("students").delete().eq("student_id", user_id).execute()
    return {"deleted": True}