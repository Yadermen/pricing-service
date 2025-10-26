from fastapi import APIRouter, HTTPException, status
from typing import List

from src.repositories.project_role import ProjectRoleCRUD
from src.schemas.project_role import ProjectRoleCreate, ProjectRoleUpdate, ProjectRoleResponse

router = APIRouter(prefix="/project-roles", tags=["Project Roles"])


@router.post(
    "/",
    response_model=ProjectRoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create project role",
    description="Create a new project role assignment"
)
async def create_project_role(project_role: ProjectRoleCreate):
    result = await ProjectRoleCRUD.create_project_role(project_role)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("comment", "Role or Project not found")
        )

    return result


@router.get(
    "/project/{project_id}",
    response_model=List[ProjectRoleResponse],
    summary="Get project roles by project ID",
    description="Get all role assignments for a specific project"
)
async def get_project_roles_by_project_id(project_id: int):
    return await ProjectRoleCRUD.get_project_roles_by_project_id(project_id)


@router.get(
    "/{project_role_id}",
    response_model=ProjectRoleResponse,
    summary="Get project role by ID",
    description="Get a specific project role assignment by its ID"
)
async def get_project_role_by_id(project_role_id: int):
    result = await ProjectRoleCRUD.get_project_role_by_id(project_role_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project role not found"
        )

    return result


@router.put(
    "/{project_role_id}",
    response_model=ProjectRoleResponse,
    summary="Update project role",
    description="Update an existing project role assignment"
)
async def update_project_role(project_role_id: int, project_role_update: ProjectRoleUpdate):
    result = await ProjectRoleCRUD.update_project_role(project_role_id, project_role_update)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Project role not found")
        )

    return result


@router.delete(
    "/{project_role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project role",
    description="Delete a project role assignment"
)
async def delete_project_role(project_role_id: int):
    result = await ProjectRoleCRUD.delete_project_role(project_role_id)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Project role not found")
        )