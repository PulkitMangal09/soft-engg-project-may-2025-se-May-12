from fastapi import HTTPException
from ..config import supabase
from typing import Optional, Dict, Any


def get_user_id_from_token(token: str) -> str:
    """Extract user ID from authentication token."""
    auth_res = supabase.auth.get_user(token)
    if getattr(auth_res, 'error', None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return auth_res.user.id


def get_user_data(user_id: str) -> Dict[str, Any]:
    """Get user data from users table."""
    resp = supabase.table("users").select(
        "*").eq("user_id", user_id).single().execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return data


def get_user_type(user_id: str) -> str:
    """Get user type from users table."""
    user_data = get_user_data(user_id)
    return user_data.get('user_type')


def check_profile_exists(user_id: str, user_type: str) -> bool:
    """Check if user profile exists in the respective table."""
    table_map = {
        'student': 'students',
        'teacher': 'teachers',
        'parent': 'parents'
    }

    table_name = table_map.get(user_type)
    if not table_name:
        raise HTTPException(status_code=400, detail="Invalid user type")

    # Different ID field names for different user types
    id_field_map = {
        'student': 'student_id',
        'teacher': 'teacher_id',
        'parent': 'user_id'  # Parents use user_id as foreign key
    }

    id_field = id_field_map.get(user_type)
    if not id_field:
        raise HTTPException(status_code=400, detail="Invalid user type")

    try:
        resp = supabase.table(table_name).select(
            "*").eq(id_field, user_id).single().execute()
        data = getattr(resp, 'data', None)
        return data is not None
    except Exception:
        return False


def get_profile_data(user_id: str, user_type: str) -> Optional[Dict[str, Any]]:
    """Get user profile data from the respective table."""
    table_map = {
        'student': 'students',
        'teacher': 'teachers',
        'parent': 'parents'
    }

    table_name = table_map.get(user_type)
    if not table_name:
        return None

    # Different ID field names for different user types
    id_field_map = {
        'student': 'student_id',
        'teacher': 'teacher_id',
        'parent': 'user_id'  # Parents use user_id as foreign key
    }

    id_field = id_field_map.get(user_type)
    if not id_field:
        return None

    try:
        resp = supabase.table(table_name).select(
            "*").eq(id_field, user_id).single().execute()
        data = getattr(resp, 'data', None)
        return data
    except Exception:
        return None


def create_profile(user_id: str, user_type: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create user profile in the respective table."""
    table_map = {
        'student': 'students',
        'teacher': 'teachers',
        'parent': 'parents'
    }

    table_name = table_map.get(user_type)
    if not table_name:
        raise HTTPException(status_code=400, detail="Invalid user type")

    # Get user data for additional fields
    user_data = get_user_data(user_id)

    # Different ID field names and additional data for different user types
    if user_type == 'student':
        payload = {
            'student_id': user_id,
            'email': user_data.get('email'),
            'name': user_data.get('full_name'),
            **profile_data
        }
    elif user_type == 'teacher':
        payload = {
            'teacher_id': user_id,
            **profile_data
        }
    elif user_type == 'parent':
        payload = {
            'user_id': user_id,  # Use user_id as foreign key
            'name': user_data.get('full_name'),
            **profile_data
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")

    resp = supabase.table(table_name).insert(payload).execute()
    data = getattr(resp, 'data', None)
    if not data:
        raise HTTPException(status_code=400, detail="Profile creation failed")

    return data[0]
