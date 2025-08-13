from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase

router = APIRouter(prefix="/users", tags=["users"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/profile", response_model=dict)
def profile(token: str = Depends(oauth2)):
    u = supabase.auth.get_user(token)
    user_id = getattr(u.user, 'id', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    resp = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return data

@router.get("/me", response_model=dict)
def me(token: str = Depends(oauth2)):
    u = supabase.auth.get_user(token)
    user_id = getattr(u.user, 'id', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    resp = (
        supabase
        .table("users")
        .select("user_id, full_name, email, user_type")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return data