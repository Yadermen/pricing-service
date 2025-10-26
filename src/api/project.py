from fastapi import APIRouter, HTTPException, status
from typing import List

from src.repositories.project import ProjectCRUD
from src.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create project",
    description="Create a new project"
)
async def create_project(project: ProjectCreate):
    result = await ProjectCRUD.create_project(project)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to create project")
        )

    return result


@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="Get all projects",
    description="Get a list of all projects"
)
async def get_projects():
    return await ProjectCRUD.get_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
    description="Get a specific project by its ID"
)
async def get_project_by_id(project_id: int):
    result = await ProjectCRUD.get_project_by_id(project_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return result


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
    description="Update an existing project"
)
async def update_project(project_id: int, project_update: ProjectUpdate):
    result = await ProjectCRUD.update_project(project_id, project_update)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Project not found")
        )

    return result


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project",
    description="Delete a project"
)
async def delete_project(project_id: int):
    result = await ProjectCRUD.delete_project(project_id)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Project not found")
        )