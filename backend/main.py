from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.roles import router as roles_router
from app.routers.teacher_dashboard import router as dashboard_router
from app.routers.teacher_students import router as students_router
from app.routers.teacher_tasks import router as tasks_router
from app.routers.teacher_reports import router as reports_router

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