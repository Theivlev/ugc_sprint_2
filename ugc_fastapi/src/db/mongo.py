from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import settings

mongo_client: AsyncIOMotorClient | None = None


def get_mongo_db() -> AsyncIOMotorDatabase:
    """Возвращает объект базы данных MongoDB."""
    if mongo_client is None:
        raise ValueError("MongoDB клиент не инициализирован")

    return mongo_client[settings.mongo_db]