from sqlalchemy import select

from src.db.models import ProjectRoleModel
from src.db.database import  new_async_session
from src.services.cache import (invalidate_project_roles_cache_by_project_id,
                                get_cached_project_roles_by_project_id,
                                set_cached_project_roles_by_project_id,
                                get_cached_project_role_by_id,
                                set_cached_project_role_by_id,
                                invalidate_project_role_cache_by_id,
                                )

class ProjectRoleCRUD:
    @staticmethod
    async def create_project_role(project_id:int, role_id:int, count:int, custom_rate:int = None):
        async with new_async_session() as session:
            new_project_role = ProjectRoleModel(project_id=project_id, role_id=role_id, custom_rate=custom_rate, count=count)
            session.add(new_project_role)
            await session.commit()
            await invalidate_project_roles_cache_by_project_id(project_id)
            return new_project_role
    @staticmethod
    async def update_project_role(project_role_id:int, project_id:int, role_id:int,count:int, custom_rate:int = None):
        async with new_async_session() as session:
            old_project_role = await session.get(ProjectRoleModel, project_role_id)
            if old_project_role:
                old_project_role.project_id = project_id
                old_project_role.role_id = role_id
                old_project_role.custom_rate = custom_rate
                old_project_role.count = count
                await session.commit()
                await invalidate_project_roles_cache_by_project_id(project_id)
                await invalidate_project_role_cache_by_id(project_role_id)
                return old_project_role
            else:
                return {"ok":False, "message": "Project role not found"}
    @staticmethod
    async def get_project_roles_by_project_id(project_id:int):
        cached = await get_cached_project_roles_by_project_id(project_id)
        if cached:
            return cached

        async with new_async_session() as session:
            query = select(ProjectRoleModel).filter_by(project_id=project_id)
            result = await session.execute(query)
            project_roles = result.scalars().all()

            project_roles_data = [
                {
                    "id": pr.id,
                    "project_id": pr.project_id,
                    "role_id": pr.role_id,
                    "count": pr.count,
                    "custom_rate": pr.custom_rate
                } for pr in project_roles
            ]
            await set_cached_project_roles_by_project_id(project_id, project_roles_data)
            return project_roles_data


    @staticmethod
    async def get_project_role_by_id(project_role_id:int):
        cached = await get_cached_project_role_by_id(project_role_id)
        if cached:
            return cached

        async with new_async_session() as session:
            project_role = await session.get(ProjectRoleModel, project_role_id)
            if not project_role:
                return None
            project_role_data = {
                "id": project_role.id,
                "project_id": project_role.project_id,
                "role_id": project_role.role_id,
                "count": project_role.count,
                "custom_rate": project_role.custom_rate
            }
            await set_cached_project_role_by_id(project_role_id, project_role_data)
            return project_role_data


    @staticmethod
    async def delete_project_role(project_role_id:int):
        async with new_async_session() as session:
            old_project_role = await session.get(ProjectRoleModel, project_role_id)
            if old_project_role:
                await session.delete(old_project_role)
                await session.commit()
                await invalidate_project_roles_cache_by_project_id(old_project_role.project_id)
                await invalidate_project_role_cache_by_id(project_role_id)
                return {"ok":True}
            else:
                return {"ok":False, "message": "Project role not found"}