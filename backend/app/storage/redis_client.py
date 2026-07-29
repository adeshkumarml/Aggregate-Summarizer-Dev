from redis.asyncio import Redis
from app.config.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, REDIS_SSL, REDIS_TTL_SECS
import json


class RedisClient:

    def __init__(self):
        self.client = Redis(
            host = REDIS_HOST,
            port = REDIS_PORT,
            db = REDIS_DB,
            password = REDIS_PASSWORD,
            ssl = REDIS_SSL,
            decode_responses = True
        )

    async def save_job(self, key: str, value: str):
        await self.client.setex(key, REDIS_TTL_SECS, value)


    async def get_job(self, key: str) -> dict | None:
        data = await self.client.get(key)
        if data is None:
            return None
        return json.loads(data)


    async def delete_job(self, key: str):
        await self.client.delete(key)


    async def health_check(self) -> bool:
        try:
            await self.client.ping()
            return True

        except Exception:
            return False


    async def close(self):
        await self.client.close()


redis_client = RedisClient()