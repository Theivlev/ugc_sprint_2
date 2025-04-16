from datetime import datetime
from typing import List

from beanie import Document
from pydantic import Field
from src.models.mixins import PyObjectId


class UserBookmarks(Document):
    """
    Модель для коллекции 'user_bookmarks'.
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    movie_id: PyObjectId
    user_id: PyObjectId
    bookmarked_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "user_bookmarks"

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
