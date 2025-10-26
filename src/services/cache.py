import logging
import redis.asyncio as redis
import json
from redis import RedisError

from src.config import cache_settings

redis_client = redis.Redis(
    host=cache_settings.REDIS_HOST,
    port=cache_settings.REDIS_PORT,
    db=cache_settings.REDIS_DB,
    decode_responses=True
)




async def get_cached_roles():
    try:
        cached = await redis_client.get(cache_settings.CACHE_ROLES_KEY)
        if cached:
            return json.loads(cached)
        return None
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in get_cached_roles: {e}")
        return None
    except RedisError as e:
        logging.error(f"Redis error in get_cached_roles: {e}")
        return None

async def set_cached_roles(roles: list):
    try:
        await redis_client.set(cache_settings.CACHE_ROLES_KEY, json.dumps(roles), ex=cache_settings.CACHE_TTL)
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in set_cached_roles: {e}")
    except RedisError as e:
        logging.error(f"Redis error in set_cached_roles: {e}")

async def invalidate_roles_cache():
    try:
        await redis_client.delete(cache_settings.CACHE_ROLES_KEY)
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in invalidate_roles_cache: {e}")
    except RedisError as e:
        logging.error(f"Redis error in invalidate_roles_cache: {e}")

def project_roles_cache_key(project_id: int) -> str:
    return f"{cache_settings.CACHE_PROJECT_ROLES_PREFIX}{project_id}"

def project_role_cache_key(project_role_id: int) -> str:
    return f"{cache_settings.CACHE_PROJECT_ROLE_PREFIX}{project_role_id}"

async def get_cached_project_roles_by_project_id(project_id: int):
    key = project_roles_cache_key(project_id)
    try:
        cached = await redis_client.get(key)
        if cached:
            return json.loads(cached)
        return None
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in get_cached_project_roles_by_project_id: {e}")
        return None
    except RedisError as e:
        logging.error(f"Redis error in get_cached_project_roles_by_project_id: {e}")
        return None

async def set_cached_project_roles_by_project_id(project_id: int, project_roles_data: list):
    key = project_roles_cache_key(project_id)
    try:
        await redis_client.set(key, json.dumps(project_roles_data), ex=cache_settings.CACHE_TTL)
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in set_cached_project_roles_by_project_id: {e}")
    except RedisError as e:
        logging.error(f"Redis error in set_cached_project_roles_by_project_id: {e}")

async def invalidate_project_roles_cache_by_project_id(project_id: int):
    key = project_roles_cache_key(project_id)
    try:
        await redis_client.delete(key)
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in invalidate_project_roles_cache_by_project_id: {e}")
    except RedisError as e:
        logging.error(f"Redis error in invalidate_project_roles_cache_by_project_id: {e}")

async def get_cached_project_role_by_id(project_role_id: int):
    key = project_role_cache_key(project_role_id)
    try:
        cached = await redis_client.get(key)
        if cached:
            return json.loads(cached)
        return None
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in get_cached_project_role_by_id: {e}")
        return None
    except RedisError as e:
        logging.error(f"Redis error in get_cached_project_role_by_id: {e}")
        return None

async def set_cached_project_role_by_id(project_role_id: int, project_role_data: dict):
    key = project_role_cache_key(project_role_id)
    try:
        await redis_client.set(key, json.dumps(project_role_data), ex=cache_settings.CACHE_TTL)
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in set_cached_project_role_by_id: {e}")
    except RedisError as e:
        logging.error(f"Redis error in set_cached_project_role_by_id: {e}")

async def invalidate_project_role_cache_by_id(project_role_id: int):
    key = project_role_cache_key(project_role_id)
    try:
        await redis_client.delete(key)
    except (ConnectionError, TimeoutError) as e:
        logging.error(f"Redis connection issue in invalidate_project_role_cache_by_id: {e}")
    except RedisError as e:
        logging.error(f"Redis error in invalidate_project_role_cache_by_id: {e}")

