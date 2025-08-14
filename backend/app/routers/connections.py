from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any, Optional

from ..config import supabase
from ..utils.profile_utils import get_user_id_from_token

router = APIRouter(prefix="/connections", tags=["connections"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.get("/")
def list_connections(
    token: str = Depends(oauth2),
    type: Optional[str] = Query(default=None),
    debug: Optional[int] = Query(default=None),
) -> List[Dict[str, Any]]:
    """List connections for the caller built from classroom/family sources, enriched with partner fields.

    Supports type filter: teacher_student | parent_student | family
    """
    user_id = get_user_id_from_token(token)

    # Caller profile (to get email/user_type)
    me_res = (
        supabase.table("users")
        .select("user_id, email, user_type, full_name")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    me = getattr(me_res, "data", None) or {}
    my_email = me.get("email")
    my_type = me.get("user_type")

    # Helper to batch fetch user profiles
    def fetch_users(uids: List[str]) -> Dict[str, Dict[str, Any]]:
        if not uids:
            return {}
        resp = (
            supabase.table("users")
            .select("user_id, full_name, email, user_type")
            .in_("user_id", list(set([u for u in uids if u])))
            .execute()
        )
        out: Dict[str, Dict[str, Any]] = {}
        for r in getattr(resp, "data", []) or []:
            uid = r.get("user_id")
            if uid:
                out[uid] = r
        return out

    teacher_items: List[Dict[str, Any]] = []
    parent_items: List[Dict[str, Any]] = []
    family_items: List[Dict[str, Any]] = []
    # debug vars
    dbg_my_memberships: List[Dict[str, Any]] = []
    dbg_family_ids: List[str] = []
    dbg_student_families: List[str] = []
    dbg_parent_members_count: int = 0

    # Build teacher_student connections when caller is a student
    try:
        # Resolve student_id via email if available
        student_id = None
        if my_email:
            sres = (
                supabase.table("students")
                .select("student_id")
                .eq("email", my_email)
                .limit(1)
                .execute()
            )
            student_id = (getattr(sres, "data", []) or [{}])[0].get("student_id") if (getattr(sres, "data", []) or []) else None

        if student_id:
            # Find classroom enrollments for this student
            enr = (
                supabase.table("classroom_students")
                .select("classroom_id, enrolled_at, is_active")
                .eq("student_id", student_id)
                .eq("is_active", True)
                .execute()
            )
            enrollments = getattr(enr, "data", []) or []
            classroom_ids = [e.get("classroom_id") for e in enrollments if e.get("classroom_id")]
            cls = []
            if classroom_ids:
                cls = (
                    supabase.table("classrooms")
                    .select("classroom_id, teacher_id, created_at")
                    .in_("classroom_id", classroom_ids)
                    .execute()
                    .data
                    or []
                )
            teacher_ids = [c.get("teacher_id") for c in cls if c.get("teacher_id")]
            tmap = fetch_users(teacher_ids)
            # fetch teacher metadata (school, subject, etc.)
            teachers_meta = []
            if teacher_ids:
                teachers_meta = (
                    supabase.table("teachers")
                    .select("teacher_id, school_name, school_district, subject_grade, is_approved, approval_date")
                    .in_("teacher_id", teacher_ids)
                    .execute()
                    .data
                    or []
                )
            tmeta_map = {t.get("teacher_id"): t for t in teachers_meta}
            for e in enrollments:
                c = next((x for x in cls if x.get("classroom_id") == e.get("classroom_id")), None)
                tid = c.get("teacher_id") if c else None
                prof = tmap.get(tid or "", {})
                meta = tmeta_map.get(tid or "", {})
                teacher_items.append({
                    "connection_type": "teacher_student",
                    "partner_id": tid,
                    "partner_name": prof.get("full_name"),
                    "email": prof.get("email"),
                    "user_type": prof.get("user_type"),
                    "display_role": prof.get("user_type"),
                    "classroom_id": e.get("classroom_id"),
                    "established_at": e.get("enrolled_at") or (c.get("created_at") if c else None),
                    # teacher metadata
                    "school_name": meta.get("school_name"),
                    "school_district": meta.get("school_district"),
                    "subject_grade": meta.get("subject_grade"),
                    "teacher_is_approved": meta.get("is_approved"),
                    "teacher_approval_date": meta.get("approval_date"),
                })
    except Exception:
        teacher_items = []

    # Build parent_student connections from family memberships (caller as child)
    try:
        # Find families where the current user is a member
        fam_rows = (
            supabase.table("family_members")
            .select("family_id, role, relationship_type, joined_at, is_active")
            .eq("user_id", user_id)  # user_id from token matches family_members.user_id
            .execute()
        )
        my_memberships = getattr(fam_rows, "data", []) or []
        # treat null is_active as True
        my_memberships = [m for m in my_memberships if m.get("is_active", True)]
        family_ids = [m.get("family_id") for m in my_memberships if m.get("family_id")]
        
        # capture debug
        dbg_my_memberships = my_memberships[:]
        dbg_family_ids = family_ids[:]

        if family_ids:
            # Get ALL family members from the user's families (excluding self)
            all_family_members = (
                supabase.table("family_members")
                .select("family_id, user_id, role, relationship_type, joined_at, is_active")
                .in_("family_id", family_ids)
                .neq("user_id", user_id)  # exclude self
                .execute()
                .data
                or []
            )
            
            # Filter active members
            active_family_members = [
                fm for fm in all_family_members 
                if fm.get("is_active", True) and fm.get("user_id")
            ]
            
            dbg_parent_members_count = len(active_family_members)
            
            # Get user profiles for all family members
            member_ids = [fm.get("user_id") for fm in active_family_members if fm.get("user_id")]
            member_profiles = fetch_users(member_ids)
            
            # Create parent_student connections
            for fm in active_family_members:
                prof = member_profiles.get(fm.get("user_id") or "", {})
                
                # Determine display role - prefer family role, fallback to user_type
                display_role = fm.get("role") or prof.get("user_type") or "Family Member"
                
                parent_items.append({
                    "connection_type": "parent_student",
                    "partner_id": fm.get("user_id"),
                    "partner_name": prof.get("full_name"),
                    "email": prof.get("email"),
                    "user_type": prof.get("user_type"),
                    "display_role": display_role,
                    "family_id": fm.get("family_id"),
                    "family_name": None,  # Could be populated from family_groups if needed
                    "relationship_type": fm.get("relationship_type"),
                    "established_at": fm.get("joined_at"),
                })

    except Exception as e:
        print(f"Error building parent connections: {e}")
        parent_items = []

    # FIXED: Build family connections (family heads and group info)
    try:
        if family_ids:
            # Get family group details including family head
            family_groups = (
                supabase.table("family_groups")
                .select("family_id, family_name, family_head_id, created_at, is_active")
                .in_("family_id", family_ids)
                .eq("is_active", True)
                .execute()
                .data
                or []
            )
            
            # Get family head profiles
            head_ids = [fg.get("family_head_id") for fg in family_groups if fg.get("family_head_id")]
            head_profiles = fetch_users(head_ids)
            
            for fg in family_groups:
                head_id = fg.get("family_head_id")
                # Only show family head if it's not the current user
                if head_id and head_id != user_id:
                    head_prof = head_profiles.get(head_id, {})
                    family_items.append({
                        "connection_type": "family",
                        "partner_id": head_id,
                        "partner_name": head_prof.get("full_name"),
                        "email": head_prof.get("email"),
                        "user_type": head_prof.get("user_type"),
                        "display_role": "Family Head",
                        "family_id": fg.get("family_id"),
                        "family_name": fg.get("family_name"),
                        "relationship_type": "head",
                        "established_at": fg.get("created_at"),
                    })

    except Exception as e:
        print(f"Error building family connections: {e}")
        family_items = []

    # Apply type filter
    if type == "teacher_student":
        items = teacher_items
    elif type == "parent_student":
        items = parent_items
    elif type == "family":
        items = family_items
    else:
        items = teacher_items + parent_items + family_items

    if debug:
        return {
            "items": items,
            "debug": {
                "my_memberships_count": len(dbg_my_memberships),
                "my_memberships_sample": dbg_my_memberships[:3],
                "family_ids": dbg_family_ids,
                "parent_members_count": dbg_parent_members_count,
                "teacher_items_count": len(teacher_items),
                "parent_items_count": len(parent_items),
                "family_items_count": len(family_items),
            },
        }

    return items