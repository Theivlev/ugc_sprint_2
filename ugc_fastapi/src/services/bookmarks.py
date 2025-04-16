from typing import Type

from motor.motor_asyncio import AsyncIOMotorDatabase
from src.crud.base import BaseMongoCRUD
from src.db.mongo import get_mongo_db
from src.models.bookmark import UserBookmarks

from fastapi import Depends


async def get_crud_service(db: AsyncIOMotorDatabase = Depends(get_mongo_db)) -> BaseMongoCRUD:
    """
    Возвращает экземпляр CRUD-сервиса для работы с коллекцией 'user_bookmarks'.
    """
    return BaseMongoCRUD(collection=db["user_bookmarks"], model=UserBookmarks)
