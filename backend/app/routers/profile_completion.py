from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase
from ..models import (
    StudentProfileCreate, TeacherProfileCreate, ParentProfileCreate,
    ProfileCompletionResponse, ProfileStatusResponse
)
from ..utils.profile_utils import (
    get_user_id_from_token, get_user_type, check_profile_exists,
    get_profile_data, create_profile
)

router = APIRouter(prefix="/profile", tags=["profile-completion"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.get("/status", response_model=ProfileStatusResponse)
def get_profile_status(token: str = Depends(oauth2)):
    """Check if user has completed profile setup."""
    user_id = get_user_id_from_token(token)
    user_type = get_user_type(user_id)

    has_profile = check_profile_exists(user_id, user_type)
    profile_data = get_profile_data(
        user_id, user_type) if has_profile else None

    return ProfileStatusResponse(
        has_profile=has_profile,
        is_completed=has_profile,
        user_type=user_type,
        profile_data=profile_data
    )


@router.post("/student", response_model=dict)
def create_student_profile(profile: StudentProfileCreate, token: str = Depends(oauth2)):
    """Create student profile."""
    user_id = get_user_id_from_token(token)
    user_type = get_user_type(user_id)

    if user_type != 'student':
        raise HTTPException(
            status_code=403, detail="Only students can create student profiles")

    if check_profile_exists(user_id, user_type):
        raise HTTPException(
            status_code=400, detail="Student profile already exists")

    profile_data = profile.dict(exclude_unset=True)
    return create_profile(user_id, user_type, profile_data)


@router.post("/teacher", response_model=dict)
def create_teacher_profile(profile: TeacherProfileCreate, token: str = Depends(oauth2)):
    """Create teacher profile."""
    user_id = get_user_id_from_token(token)
    user_type = get_user_type(user_id)

    if user_type != 'teacher':
        raise HTTPException(
            status_code=403, detail="Only teachers can create teacher profiles")

    if check_profile_exists(user_id, user_type):
        raise HTTPException(
            status_code=400, detail="Teacher profile already exists")

    profile_data = profile.dict(exclude_unset=True)
    return create_profile(user_id, user_type, profile_data)


@router.post("/parent", response_model=dict)
def create_parent_profile(profile: ParentProfileCreate, token: str = Depends(oauth2)):
    """Create parent profile."""
    user_id = get_user_id_from_token(token)
    user_type = get_user_type(user_id)

    if user_type != 'parent':
        raise HTTPException(
            status_code=403, detail="Only parents can create parent profiles")

    if check_profile_exists(user_id, user_type):
        raise HTTPException(
            status_code=400, detail="Parent profile already exists")

    profile_data = profile.dict(exclude_unset=True)
    return create_profile(user_id, user_type, profile_data)
