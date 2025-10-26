from sqlalchemy import select

from src.db.models import RoleModel
from src.services.cache import get_cached_roles, set_cached_roles, invalidate_roles_cache
from src.db.database import  new_async_session

class RoleCRUD:
    @staticmethod
    async def create_role(name:str, default_rate:int):
        async with new_async_session() as session:
            new_role = RoleModel(name=name, default_rate=default_rate)
            session.add(new_role)
            await session.commit()
            await invalidate_roles_cache()
            return new_role
    @staticmethod
    async def get_role_by_id(role_id:int):
        async with new_async_session() as session:
            query = select(RoleModel).filter_by(id=role_id)
            result = await session.execute(query)
            role = result.scalar()
            return role
    @staticmethod
    async def get_roles():
        cached = await get_cached_roles()
        if cached:
            return cached

        async with new_async_session() as session:
            query = select(RoleModel)
            result = await session.execute(query)
            roles = result.scalars().all()

            roles_data = [{"id": r.id, "name": r.name, "default_rate": r.default_rate} for r in roles]
            await set_cached_roles(roles_data)
            return roles_data
    @staticmethod
    async def update_role(id:int, name:str, default_rate:int):
        async with new_async_session() as session:
            old_role = await session.get(RoleModel, id)
            if old_role:
                old_role.name = name
                old_role.default_rate = default_rate
                await session.commit()
                await invalidate_roles_cache()
                return old_role
            else:
                return {"ok":False, "message": "Role not found"}
    @staticmethod
    async def delete_role(role_id:int):
        async with new_async_session() as session:
            old_role = await session.get(RoleModel, role_id)
            if old_role:
                await session.delete(old_role)
                await session.commit()
                await invalidate_roles_cache()
                return {"ok":True}
            else:
                return {"ok":False, "message": "Role not found"}