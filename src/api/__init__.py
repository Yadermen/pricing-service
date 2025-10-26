from fastapi import APIRouter

from src.api.role import router as role_router
from src.api.project import router as project_router
from src.api.project_role import router as project_role_router
from src.api.calculator import router as calculator_router

main_router = APIRouter()

main_router.include_router(project_router)
main_router.include_router(role_router)
main_router.include_router(project_role_router)
main_router.include_router(calculator_router)