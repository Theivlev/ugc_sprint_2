from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.bookmark import UserBookmarks
from src.core.config import project_settings

async def init_db(db):
    """
    Инициализация Beanie с MongoDB.
    """
    await init_beanie(database=db, document_models=[UserBookmarks])
