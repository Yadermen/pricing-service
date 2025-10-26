from pydantic import BaseModel, Field
from typing import Optional
from src.schemas.project import ProjectResponse
from src.schemas.role import RoleResponse


class ProjectRoleBase(BaseModel):
    project_id: int = Field(..., description="Project ID")
    role_id: int = Field(..., description="Role ID")
    count: int = Field(default=0, ge=0, description="Number of people in this role")


class ProjectRoleCreate(ProjectRoleBase):
    custom_rate: Optional[int] = Field(None, ge=0, description="Custom hourly rate for this project")


class ProjectRoleUpdate(BaseModel):
    custom_rate: Optional[int] = Field(None, ge=0, description="Custom hourly rate")
    count: Optional[int] = Field(None, ge=0, description="Number of people")


class ProjectRoleResponse(ProjectRoleBase):
    id: int
    custom_rate: Optional[int]

    class Config:
        from_attributes = True


class ProjectRoleWithDetails(ProjectRoleResponse):
    project: ProjectResponse
    role: RoleResponse