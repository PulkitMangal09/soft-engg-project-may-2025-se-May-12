from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from fastapi import HTTPException

from ..config import supabase

# ---- Auth helpers ----


def get_user_id_from_token(token: str) -> str:
    """Return the authenticated user's id (or 401)."""
    try:
        res = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = getattr(res, "user", None)
    if not user or not getattr(user, "id", None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user.id


def _get_row(table: str, key: str, value: str) -> Optional[Dict[str, Any]]:
    r = supabase.table(table).select("*").eq(key, value).single().execute()
    return getattr(r, "data", None)


def get_user_type(user_id: str) -> str:
    """
    Returns one of: 'student' | 'teacher' | 'parent'
    Tries `profiles.role` first, falls back to `users.user_type`.
    """
    # Preferred: profiles table
    prof = _get_row("users", "user_id", user_id)
    role = (prof or {}).get("user_type")
    if isinstance(role, str) and role:
        return role

    # Fallback: users.user_type
    user = _get_row("users", "user_id", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    ut = user.get("user_type")
    if not ut:
        raise HTTPException(status_code=400, detail="User has no type")
    return ut


# ---- Optional profile helpers (if you still use per-role tables) ----

_TABLE_MAP = {"student": "students",
              "teacher": "teachers", "parent": "parents"}
_ID_FIELD = {"student": "student_id",
             "teacher": "teacher_id", "parent": "user_id"}


def check_profile_exists(user_id: str, user_type: str) -> bool:
    table = _TABLE_MAP.get(user_type)
    key = _ID_FIELD.get(user_type)
    if not table or not key:
        raise HTTPException(status_code=400, detail="Invalid user type")
    try:
        data = _get_row(table, key, user_id)
        return data is not None
    except Exception:
        return False


def get_profile_data(user_id: str, user_type: str) -> Optional[Dict[str, Any]]:
    table = _TABLE_MAP.get(user_type)
    key = _ID_FIELD.get(user_type)
    if not table or not key:
        return None
    try:
        return _get_row(table, key, user_id)
    except Exception:
        return None


def get_user_data(user_id: str) -> Dict[str, Any]:
    user = _get_row("users", "user_id", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_profile(user_id: str, user_type: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    table = _TABLE_MAP.get(user_type)
    key = _ID_FIELD.get(user_type)
    if not table or not key:
        raise HTTPException(status_code=400, detail="Invalid user type")

    user_data = get_user_data(user_id)

    if user_type == "student":
        payload = {
            "student_id": user_id,
            "email": user_data.get("email"),
            "name": user_data.get("full_name"),
            **profile_data,
        }
    elif user_type == "teacher":
        payload = {"teacher_id": user_id, **profile_data}
    elif user_type == "parent":
        payload = {"user_id": user_id, "name": user_data.get(
            "full_name"), **profile_data}
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")

    resp = supabase.table(table).insert(payload).execute()
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Profile creation failed")
    return data[0]


def update_profile(user_id: str, user_type: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing profile row for the given user and type.

    Only fields provided in profile_data will be updated.
    """
    table = _TABLE_MAP.get(user_type)
    key = _ID_FIELD.get(user_type)
    if not table or not key:
        raise HTTPException(status_code=400, detail="Invalid user type")

    # Ensure profile exists before updating
    if not check_profile_exists(user_id, user_type):
        raise HTTPException(status_code=404, detail="Profile not found")

    # Never allow changing the owner id key through update payload
    safe_payload = {k: v for k, v in profile_data.items() if k != key}
    if not safe_payload:
        # No-op update should still return the existing row
        existing = get_profile_data(user_id, user_type)
        if not existing:
            raise HTTPException(status_code=404, detail="Profile not found")
        return existing

    resp = (
        supabase
        .table(table)
        .update(safe_payload)
        .eq(key, user_id)
        .execute()
    )
    data = getattr(resp, "data", None)
    if not data:
        raise HTTPException(status_code=400, detail="Profile update failed")
    return data[0]
