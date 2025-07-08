from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.roles import router as roles_router
from app.routers.teacher_dashboard import router as dashboard_router
from app.routers.teacher_students import router as students_router
from app.routers.teacher_tasks import router as tasks_router
from app.routers.teacher_reports import router as reports_router
from app.routers.student_dashboard import router as student_dashboard_router
from app.routers.student_tasks import router as student_tasks_router
from app.routers.student_finance import router as student_finance_router
from app.routers.student_emotions import router as student_emotions_router
from app.routers.student_diet import router as student_diet_router
from app.routers.student_health import router as student_health_router
from app.routers.parent_dashboard import router as parent_dashboard_router
from app.routers.parent_children import router as parent_children_router
from app.routers.parent_requests import router as parent_requests_router
from app.routers.parent_tasks import router as parent_tasks_router
from app.routers.parent_family import router as parent_family_router

app = FastAPI(
    title="GrowthGeine API",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(dashboard_router)
app.include_router(students_router)
app.include_router(tasks_router)
app.include_router(reports_router)
app.include_router(student_dashboard_router)
app.include_router(student_tasks_router)
app.include_router(student_finance_router)
app.include_router(student_emotions_router)
app.include_router(student_diet_router)
app.include_router(student_health_router)
app.include_router(parent_dashboard_router)
app.include_router(parent_children_router)
app.include_router(parent_requests_router)
app.include_router(parent_tasks_router)
app.include_router(parent_family_router)