from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import project_settings
from src.models.bookmark import UserBookmarks


async def init_db(db):
    """
    Инициализация Beanie с MongoDB.
    """
    await init_beanie(database=db, document_models=[UserBookmarks])
