from fastapi import APIRouter, HTTPException, status
from typing import List

from src.repositories.role import RoleCRUD
from src.schemas.role import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post(
    "/",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create role",
    description="Create a new role"
)
async def create_role(role: RoleCreate):
    result = await RoleCRUD.create_role(role)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to create role")
        )

    return result


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Get role by ID",
    description="Get a specific role by its ID"
)
async def get_role_by_id(role_id: int):
    result = await RoleCRUD.get_role_by_id(role_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    return result


@router.get(
    "/",
    response_model=List[RoleResponse],
    summary="Get all roles",
    description="Get a list of all roles"
)
async def get_roles():
    return await RoleCRUD.get_roles()


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Update role",
    description="Update an existing role"
)
async def update_role(role_id: int, role_update: RoleUpdate):
    result = await RoleCRUD.update_role(role_id, role_update)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Role not found")
        )

    return result


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete role",
    description="Delete a role"
)
async def delete_role(role_id: int):
    result = await RoleCRUD.delete_role(role_id)

    if isinstance(result, dict) and not result.get("ok", True):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Role not found")
        )