from pydantic import BaseModel, Field
from typing import Optional


class RoleBase(BaseModel):
    name: str = Field(..., max_length=255, description="Role name")
    default_rate: int = Field(..., ge=0, description="Default hourly rate")


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Role name")
    default_rate: Optional[int] = Field(None, ge=0, description="Default hourly rate")


class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True