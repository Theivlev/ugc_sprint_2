from datetime import datetime

from beanie import Document
from pydantic import Field
from src.models.mixins import PyObjectId


class UserLike(Document):
    """Модель для коллекции 'user_likes'."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    movie_id: PyObjectId
    user_id: PyObjectId
    rating: int = Field(..., ge=1, le=10)
    liked_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "user_likes"
