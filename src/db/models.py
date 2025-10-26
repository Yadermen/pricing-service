import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import  Base

class ProjectModel(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    coefficient: Mapped[float] = mapped_column(Float(precision=2))
    total_price: Mapped[int] = mapped_column(nullable=True, default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

class RoleModel(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    default_rate: Mapped[int] = mapped_column()

class ProjectRoleModel(Base):
    __tablename__ = "project_roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    custom_rate: Mapped[int] = mapped_column(nullable=True)
    count: Mapped[int] = mapped_column(default=0)
