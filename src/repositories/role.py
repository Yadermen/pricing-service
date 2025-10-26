from sqlalchemy import select
from src.db.models import RoleModel
from src.services.cache import get_cached_roles, set_cached_roles, invalidate_roles_cache
from src.db.database import new_async_session
from src.schemas.role import RoleCreate, RoleUpdate, RoleResponse


class RoleCRUD:
    @staticmethod
    async def create_role(role: RoleCreate) -> RoleResponse:
        async with new_async_session() as session:
            new_role = RoleModel(name=role.name, default_rate=role.default_rate)
            session.add(new_role)
            await session.commit()
            await session.refresh(new_role)
            await invalidate_roles_cache()
            return RoleResponse.model_validate(new_role)

    @staticmethod
    async def get_role_by_id(role_id: int) -> RoleResponse | None:
        async with new_async_session() as session:
            query = select(RoleModel).filter_by(id=role_id)
            result = await session.execute(query)
            role = result.scalar()
            if role:
                return RoleResponse.model_validate(role)
            return None

    @staticmethod
    async def is_role(role_id: int) -> bool:
        async with new_async_session() as session:
            query = select(RoleModel).filter_by(id=role_id)
            result = await session.execute(query)
            role = result.scalar_one_or_none()
            if role is None:
                return False
            else:
                return True

    @staticmethod
    async def get_roles() -> list[RoleResponse]:
        cached = await get_cached_roles()
        if cached:
            return [RoleResponse(**role_data) for role_data in cached]

        async with new_async_session() as session:
            query = select(RoleModel)
            result = await session.execute(query)
            roles = result.scalars().all()

            roles_response = [RoleResponse.model_validate(role) for role in roles]
            roles_data = [role.model_dump() for role in roles_response]
            await set_cached_roles(roles_data)
            return roles_response

    @staticmethod
    async def update_role(id: int, role_update: RoleUpdate) -> RoleResponse | dict:
        async with new_async_session() as session:
            old_role = await session.get(RoleModel, id)
            if old_role:

                update_data = role_update.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(old_role, field, value)

                await session.commit()
                await session.refresh(old_role)
                await invalidate_roles_cache()
                return RoleResponse.model_validate(old_role)
            else:
                return {"ok": False, "message": "Role not found"}

    @staticmethod
    async def delete_role(role_id: int) -> dict:
        async with new_async_session() as session:
            old_role = await session.get(RoleModel, role_id)
            if old_role:
                await session.delete(old_role)
                await session.commit()
                await invalidate_roles_cache()
                return {"ok": True}
            else:
                return {"ok": False, "message": "Role not found"}