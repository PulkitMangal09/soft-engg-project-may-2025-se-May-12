from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any, Optional

from ..config import supabase
from ..utils.profile_utils import get_user_id_from_token

router = APIRouter(prefix="/connections", tags=["connections"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.get("/")
def list_connections(token: str = Depends(oauth2), type: Optional[str] = Query(default=None)) -> List[Dict[str, Any]]:
    user_id = get_user_id_from_token(token)

    q = (
        supabase.table("user_connections")
        .select("*")
        .or_(f"user_id_1.eq.{user_id},user_id_2.eq.{user_id}")
    )
    if type:
        q = q.eq("connection_type", type)
    res = q.execute()
    return getattr(res, "data", []) or []
