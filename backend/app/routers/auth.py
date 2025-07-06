from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from gotrue.errors import AuthApiError
from ..config import supabase
from ..models import SignupRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=dict)
def signup(request: SignupRequest):
    try:
        res = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
        })
    except AuthApiError as e:
        raise HTTPException(status_code=400, detail=str(e))
    user_id = getattr(res.user, 'id', None) or res.user.get('id')
    if not user_id:
        raise HTTPException(status_code=500, detail="No user ID returned")
    supabase.table("users").insert({
        "user_id":    user_id,
        "email":      request.email,
        "full_name":  request.full_name,
        "user_type":  request.role.name,
    }).execute()
    return {"message":"Account created","user_id":user_id}

@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password,
        })
    except AuthApiError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token = getattr(res.session, 'access_token', None) or res.session.get('access_token')
    if not token:
        raise HTTPException(status_code=500, detail="No access token returned")
    return TokenResponse(access_token=token, token_type="bearer")