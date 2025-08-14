from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any, Optional

from ..config import supabase
from ..utils.profile_utils import get_user_id_from_token

router = APIRouter(prefix="/connections", tags=["connections"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.get("/")
def list_connections(token: str = Depends(oauth2), type: Optional[str] = Query(default=None)) -> List[Dict[str, Any]]:
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
        fam_rows = (
            supabase.table("family_members")
            .select("family_id, role, joined_at")
            .eq("user_id", user_id)
            .eq("is_active", True)
            .execute()
        )
        my_memberships = getattr(fam_rows, "data", []) or []
        family_ids = [m.get("family_id") for m in my_memberships if m.get("family_id")]
        child_family_ids = [m.get("family_id") for m in my_memberships if m.get("role") == "child"]

        # Parents in the same families where I'm a child
        parent_members = []
        if child_family_ids:
            parent_members = (
                supabase.table("family_members")
                .select("family_id, user_id, role, joined_at")
                .in_("family_id", child_family_ids)
                .in_("role", ["parent", "head"])
                .eq("is_active", True)
                .execute()
                .data
                or []
            )
        parent_ids = [pm.get("user_id") for pm in parent_members if pm.get("user_id")]
        pmap = fetch_users(parent_ids)
        for pm in parent_members:
            prof = pmap.get(pm.get("user_id") or "", {})
            parent_items.append({
                "connection_type": "parent_student",
                "partner_id": pm.get("user_id"),
                "partner_name": prof.get("full_name"),
                "email": prof.get("email"),
                "user_type": prof.get("user_type"),
                "display_role": prof.get("user_type"),
                "family_id": pm.get("family_id"),
                "established_at": pm.get("joined_at"),
            })

        # Family group entries for all families I'm part of
        fam_groups = []
        if family_ids:
            fam_groups = (
                supabase.table("family_groups")
                .select("family_id, name, family_name, family_head_id, created_at")
                .in_("family_id", family_ids)
                .execute()
                .data
                or []
            )
        # Map my role in each family
        role_map: Dict[str, str] = {}
        for m in my_memberships:
            fid = m.get("family_id")
            if fid and fid not in role_map:
                role_map[fid] = m.get("role")
        for fg in fam_groups:
            family_items.append({
                "connection_type": "family",
                "family_id": fg.get("family_id"),
                "family_name": fg.get("family_name") or fg.get("name"),
                "role": role_map.get(fg.get("family_id"), None),
                "established_at": fg.get("created_at"),
            })
    except Exception:
        parent_items = []
        family_items = []

    # Apply type filter
    if type == "teacher_student":
        return teacher_items
    if type == "parent_student":
        return parent_items
    if type == "family":
        return family_items

    return teacher_items + parent_items + family_items
