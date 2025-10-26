from  sqlalchemy import select

from src.db.models import ProjectModel
from src.db.database import  new_async_session


class ProjectCRUD:
    @staticmethod
    async def create_project(name:str, coefficient:float):
        async with new_async_session() as session:
            new_project = ProjectModel(name=name, coefficient=coefficient)
            session.add(new_project)
            await session.commit()
            return new_project
    @staticmethod
    async def get_project_by_id(project_id:int):
        async with new_async_session() as session:
            query = select(ProjectModel).where(ProjectModel.id == project_id)
            result = await session.execute(query)
            project = result.scalar_one_or_none()
            return project
    @staticmethod
    async def get_projects():
        async with new_async_session() as session:
            query = select(ProjectModel)
            result = await session.execute(query)
            projects = result.scalars().all()
            return projects
    @staticmethod
    async def update_project(id:int, name:str, coefficient:float):
        async with new_async_session() as session:
            old_project = await session.get(ProjectModel, id)
            if old_project:
                old_project.name = name
                old_project.coefficient = coefficient
                await session.commit()
                return old_project
            else:
                return {"ok":False, "message": "Project not found"}
    @staticmethod
    async def delete_project(id:int):
        async with new_async_session() as session:
            old_project = await session.get(ProjectModel, id)
            if old_project:
                await session.delete(old_project)
                await session.commit()
                return {"ok":True}
            else:
                return {"ok":False, "message": "Project not found"}

    @staticmethod
    async def set_project_price(project_id:int, total_price:int):
        async with new_async_session() as session:
            project = await session.get(ProjectModel, project_id)
            if project:
                project.total_price = total_price
                await session.commit()



