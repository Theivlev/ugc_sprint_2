from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.bookmark import UserBookmarks
from src.core.config import project_settings

async def init_db():
    """
    Инициализация Beanie с MongoDB.
    """
    client = AsyncIOMotorClient(str(project_settings.mongo_dsn))
    await init_beanie(database=client[project_settings.mongo_db], document_models=[UserBookmarks])
