from datetime import datetime
from src.models.mixin import PyObjectId
from pydantic import BaseModel, Field

class UserBookmarkCreateDTO(BaseModel):
    movie_id: PyObjectId
    user_id: PyObjectId
    bookmarked_at: datetime = Field(default_factory=datetime.now)

class UserBookmarkUpdateDTO(BaseModel):
    movie_id: PyObjectId | None = None
    user_id: PyObjectId | None = None
    bookmarked_at: datetime | None = None
