from datetime import datetime

from beanie import Document
from pydantic import Field
from src.models.mixins import PyObjectId


class UserReviews(Document):
    """Модель для коллекции 'user_reviews'."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    movie_id: PyObjectId
    user_id: PyObjectId
    review_text: str
    reviewed_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "user_reviews"
