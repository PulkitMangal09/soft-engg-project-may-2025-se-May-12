from fastapi import APIRouter
from ..models import Role, RoleEnum

router = APIRouter(prefix="/roles", tags=["roles"])

# Static role list
ROLES = [
    Role(id=1, name=RoleEnum.student, description="Manage tasks"),
    Role(id=2, name=RoleEnum.teacher, description="Monitor student progress"),
    Role(id=3, name=RoleEnum.parent,  description="Track children activities"),
]

@router.get("/", response_model=list[Role])
def get_roles():
    return ROLES