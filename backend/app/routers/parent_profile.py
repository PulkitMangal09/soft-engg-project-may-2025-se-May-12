from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from ..config import supabase
from ..models import ParentProfileCreate, ProfileStatusResponse
from ..utils.profile_utils import (
    get_user_id_from_token, get_user_type, check_profile_exists,
    get_profile_data, create_profile as create_profile_util
)

router = APIRouter(prefix="/parent/profile", tags=["parent-profile"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


class ParentProfileUpdate(BaseModel):
    name: Optional[str]
    group: Optional[str]
    is_head: Optional[bool]
    description: Optional[str]


@router.get("/", response_model=dict)
def get_profile(token: str = Depends(oauth2)):
    """Get the authenticated parent's profile."""
    user_id = get_user_id_from_token(token)
    profile_data = get_profile_data(user_id, 'parent')
    if not profile_data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile_data


@router.get("/status", response_model=ProfileStatusResponse)
def get_profile_status(token: str = Depends(oauth2)):
    """Check if parent profile is completed."""
    user_id = get_user_id_from_token(token)
    user_type = get_user_type(user_id)

    if user_type != 'parent':
        raise HTTPException(
            status_code=403, detail="Only parents can access parent profile")

    has_profile = check_profile_exists(user_id, user_type)
    profile_data = get_profile_data(
        user_id, user_type) if has_profile else None

    return ProfileStatusResponse(
        has_profile=has_profile,
        is_completed=has_profile,
        user_type=user_type,
        profile_data=profile_data
    )


@router.post("/", response_model=dict)
def create_profile(data: ParentProfileCreate, token: str = Depends(oauth2)):
    """Create initial parent profile."""
    user_id = get_user_id_from_token(token)
    user_type = get_user_type(user_id)

    if user_type != 'parent':
        raise HTTPException(
            status_code=403, detail="Only parents can create parent profiles")

    if check_profile_exists(user_id, user_type):
        raise HTTPException(
            status_code=400, detail="Parent profile already exists")

    profile_data = data.dict(exclude_unset=True)
    return create_profile_util(user_id, user_type, profile_data)


@router.patch("/", response_model=dict)
def update_profile(data: ParentProfileUpdate, token: str = Depends(oauth2)):
    """Update the authenticated parent's profile."""
    user_id = get_user_id_from_token(token)
    resp = supabase.table("parents").update(
        data.dict(exclude_unset=True)).eq("user_id", user_id).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Update failed")
    return data[0]


@router.delete("/", response_model=dict)
def delete_profile(token: str = Depends(oauth2)):
    """Delete the authenticated parent's profile."""
    user_id = get_user_id_from_token(token)
    supabase.table("parents").delete().eq("user_id", user_id).execute()
    return {"deleted": True}
