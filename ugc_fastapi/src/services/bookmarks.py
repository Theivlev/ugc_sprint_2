from typing import Type

from motor.motor_asyncio import AsyncIOMotorDatabase
from src.crud.base import BaseMongoCRUD
from src.db.mongo import get_mongo_db
from src.models.bookmark import UserBookmarks
from src.shemas.user_bookmarks import UserBookmarkCreateDTO, UserBookmarkUpdateDTO

from fastapi import Depends


async def get_user_bookmark_service(db: AsyncIOMotorDatabase = Depends(get_mongo_db)) -> BaseMongoCRUD:
    return BaseMongoCRUD(collection=db["user_bookmarks"], model=UserBookmarks)
