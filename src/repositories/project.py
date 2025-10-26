from sqlalchemy import select

from src.db.models import ProjectModel
from src.db.database import new_async_session
from src.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse


class ProjectCRUD:
    @staticmethod
    async def create_project(project: ProjectCreate) -> ProjectResponse:
        async with new_async_session() as session:
            new_project = ProjectModel(name=project.name, coefficient=project.coefficient)
            session.add(new_project)
            await session.commit()
            await session.refresh(new_project)
            return ProjectResponse.model_validate(new_project)

    @staticmethod
    async def get_project_by_id(project_id: int) -> ProjectResponse | None:
        async with new_async_session() as session:
            query = select(ProjectModel).where(ProjectModel.id == project_id)
            result = await session.execute(query)
            project = result.scalar_one_or_none()
            if project:
                return ProjectResponse.model_validate(project)
            return None

    @staticmethod
    async def get_projects() -> list[ProjectResponse]:
        async with new_async_session() as session:
            query = select(ProjectModel)
            result = await session.execute(query)
            projects = result.scalars().all()
            return [ProjectResponse.model_validate(project) for project in projects]

    @staticmethod
    async def update_project(id: int, project_update: ProjectUpdate) -> ProjectResponse | dict:
        async with new_async_session() as session:
            old_project = await session.get(ProjectModel, id)
            if old_project:
                # Обновляем только переданные поля
                update_data = project_update.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(old_project, field, value)

                await session.commit()
                await session.refresh(old_project)
                return ProjectResponse.model_validate(old_project)
            else:
                return {"ok": False, "message": "Project not found"}

    @staticmethod
    async def delete_project(id: int) -> dict:
        async with new_async_session() as session:
            old_project = await session.get(ProjectModel, id)
            if old_project:
                await session.delete(old_project)
                await session.commit()
                return {"ok": True}
            else:
                return {"ok": False, "message": "Project not found"}

    @staticmethod
    async def set_project_price(project_id: int, total_price: int) -> bool:
        async with new_async_session() as session:
            project = await session.get(ProjectModel, project_id)
            if project:
                project.total_price = total_price
                await session.commit()
                return True
            return False

    @staticmethod
    async def is_project(project_id: int) -> bool:
        async with new_async_session() as session:
            query = select(ProjectModel).filter_by(id=project_id)
            result = await session.execute(query)
            project = result.scalar_one_or_none()
            if project:
                return True
            else:
                return False