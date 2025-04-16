from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.core.config import project_settings


async def get_mongo_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(str(project_settings.mongo_dsn))
    try:
        yield client[project_settings.mongo_db]
    finally:
        client.close()
