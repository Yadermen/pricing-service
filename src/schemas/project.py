from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str = Field(..., max_length=255, description="Project name")
    coefficient: float = Field(..., ge=0, description="Project coefficient")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Project name")
    coefficient: Optional[float] = Field(None, ge=0, description="Project coefficient")
    total_price: Optional[int] = Field(None, ge=0, description="Total project price")


class ProjectResponse(ProjectBase):
    id: int
    total_price: Optional[int] = 0
    created_at: datetime

    class Config:
        from_attributes = True