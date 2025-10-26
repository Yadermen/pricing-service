from sqlalchemy import select

from src.db.models import ProjectRoleModel
from src.db.database import new_async_session
from src.services.cache import (invalidate_project_roles_cache_by_project_id,
                                get_cached_project_roles_by_project_id,
                                set_cached_project_roles_by_project_id,
                                get_cached_project_role_by_id,
                                set_cached_project_role_by_id,
                                invalidate_project_role_cache_by_id,
                                )
from src.repositories.role import RoleCRUD
from src.repositories.project import ProjectCRUD
from src.schemas.project_role import ProjectRoleCreate, ProjectRoleUpdate, ProjectRoleResponse


class ProjectRoleCRUD:
    @staticmethod
    async def create_project_role(project_role_data: ProjectRoleCreate):
        async with new_async_session() as session:

            if await RoleCRUD.is_role(project_role_data.role_id) and await ProjectCRUD.is_project(
                    project_role_data.project_id):
                new_project_role = ProjectRoleModel(
                    project_id=project_role_data.project_id,
                    role_id=project_role_data.role_id,
                    custom_rate=project_role_data.custom_rate,
                    count=project_role_data.count
                )
                session.add(new_project_role)
                await session.commit()
                await invalidate_project_roles_cache_by_project_id(project_role_data.project_id)
                return new_project_role
            else:
                return {"ok": False, "comment": "Role or Project Not Found"}

    @staticmethod
    async def update_project_role(project_role_id: int, project_role_data: ProjectRoleUpdate):
        async with new_async_session() as session:
            old_project_role = await session.get(ProjectRoleModel, project_role_id)
            if old_project_role:
                if project_role_data.custom_rate is not None:
                    old_project_role.custom_rate = project_role_data.custom_rate
                if project_role_data.count is not None:
                    old_project_role.count = project_role_data.count
                await session.commit()
                await invalidate_project_roles_cache_by_project_id(old_project_role.project_id)
                await invalidate_project_role_cache_by_id(project_role_id)
                return old_project_role
            else:
                return {"ok": False, "message": "Project role not found"}

    @staticmethod
    async def get_project_roles_by_project_id(project_id: int):
        cached = await get_cached_project_roles_by_project_id(project_id)
        if cached:
            return [ProjectRoleResponse(**item) for item in cached]

        async with new_async_session() as session:
            query = select(ProjectRoleModel).filter_by(project_id=project_id)
            result = await session.execute(query)
            project_roles = result.scalars().all()

            project_roles_data = [
                ProjectRoleResponse(
                    id=pr.id,
                    project_id=pr.project_id,
                    role_id=pr.role_id,
                    count=pr.count,
                    custom_rate=pr.custom_rate
                ) for pr in project_roles
            ]


            project_roles_dict = [pr.model_dump() for pr in project_roles_data]
            await set_cached_project_roles_by_project_id(project_id, project_roles_dict)
            return project_roles_data

    @staticmethod
    async def get_project_role_by_id(project_role_id: int):

        cached = await get_cached_project_role_by_id(project_role_id)
        if cached:
            return ProjectRoleResponse(**cached)

        async with new_async_session() as session:
            project_role = await session.get(ProjectRoleModel, project_role_id)
            if not project_role:
                return None

            project_role_response = ProjectRoleResponse(
                id=project_role.id,
                project_id=project_role.project_id,
                role_id=project_role.role_id,
                count=project_role.count,
                custom_rate=project_role.custom_rate
            )

            await set_cached_project_role_by_id(project_role_id, project_role_response.model_dump())
            return project_role_response

    @staticmethod
    async def delete_project_role(project_role_id: int):
        async with new_async_session() as session:
            old_project_role = await session.get(ProjectRoleModel, project_role_id)
            if old_project_role:
                await session.delete(old_project_role)
                await session.commit()
                await invalidate_project_roles_cache_by_project_id(old_project_role.project_id)
                await invalidate_project_role_cache_by_id(project_role_id)
                return {"ok": True}
            else:
                return {"ok": False, "message": "Project role not found"}