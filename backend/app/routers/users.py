from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase

router = APIRouter(prefix="/users", tags=["users"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/profile", response_model=dict)
def profile(token: str = Depends(oauth2)):
    u = supabase.auth.api.get_user(token)
    user_id = getattr(u, 'id', None) or u.get('id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    resp = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    if resp.error:
        raise HTTPException(status_code=404, detail="User not found")
    return resp.data