from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any, Optional

from ..config import supabase
from ..utils.profile_utils import get_user_id_from_token

router = APIRouter(prefix="/user", tags=["privacy-settings"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


DEFAULT_SETTINGS = {
    "health_data_sharing": False,
    "academic_data_sharing": False,
    "financial_data_sharing": False,
    "connection_notifications": True,
}


def _get_settings_row(user_id: str) -> Optional[Dict[str, Any]]:
    res = (
        supabase.table("privacy_settings")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    return getattr(res, "data", None)


@router.get("/privacy-settings")
def get_privacy_settings(token: str = Depends(oauth2)) -> Dict[str, Any]:
    """Return privacy settings for the authenticated user.

    If no row exists yet, return sensible defaults.
    """
    user_id = get_user_id_from_token(token)
    row = _get_settings_row(user_id)
    if not row:
        return {"settings": DEFAULT_SETTINGS}

    return {
        "settings": {
            "health_data_sharing": bool(row.get("health_data_sharing", False)),
            "academic_data_sharing": bool(row.get("academic_data_sharing", False)),
            "financial_data_sharing": bool(row.get("financial_data_sharing", False)),
            "connection_notifications": bool(row.get("connection_notifications", True)),
        }
    }


@router.patch("/privacy-settings")
def patch_privacy_settings(payload: Dict[str, Any], token: str = Depends(oauth2)) -> Dict[str, Any]:
    """Upsert privacy settings for the authenticated user."""
    user_id = get_user_id_from_token(token)

    # Validate booleans (ignore unknown keys)
    def as_bool(key: str, default: bool) -> bool:
        if key in payload:
            v = payload[key]
            if isinstance(v, bool):
                return v
            raise HTTPException(status_code=422, detail=f"{key} must be boolean")
        return default

    current = _get_settings_row(user_id) or {}

    settings = {
        "user_id": user_id,
        "health_data_sharing": as_bool("health_data_sharing", current.get("health_data_sharing", DEFAULT_SETTINGS["health_data_sharing"])),
        "academic_data_sharing": as_bool("academic_data_sharing", current.get("academic_data_sharing", DEFAULT_SETTINGS["academic_data_sharing"])),
        "financial_data_sharing": as_bool("financial_data_sharing", current.get("financial_data_sharing", DEFAULT_SETTINGS["financial_data_sharing"])),
        "connection_notifications": as_bool("connection_notifications", current.get("connection_notifications", DEFAULT_SETTINGS["connection_notifications"])),
    }

    # Upsert (insert or update)
    # Supabase Python client lacks a direct upsert; we'll try update then insert if missing
    updated = (
        supabase.table("privacy_settings")
        .update(settings)
        .eq("user_id", user_id)
        .execute()
    )
    if not getattr(updated, "data", None):
        # Insert when no existing row
        ins = (
            supabase.table("privacy_settings")
            .insert(settings)
            .execute()
        )
        if not getattr(ins, "data", None):
            raise HTTPException(status_code=400, detail="Failed to update privacy settings")

    return {"settings": {
        "health_data_sharing": settings["health_data_sharing"],
        "academic_data_sharing": settings["academic_data_sharing"],
        "financial_data_sharing": settings["financial_data_sharing"],
        "connection_notifications": settings["connection_notifications"],
    }}
