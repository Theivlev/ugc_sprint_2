from datetime import datetime

from pydantic import BaseModel, Field, validator
from src.models.dto import AbstractDTO
from src.models.mixins import PyObjectId


class UserBookmarkCreateDTO(AbstractDTO):
    movie_id: PyObjectId | str
    user_id: PyObjectId | str
    bookmarked_at: datetime = Field(default_factory=datetime.now)

    @validator("movie_id", "user_id", pre=True)
    def validate_object_id(cls, value):
        if not PyObjectId.is_valid(value):
            raise ValueError("Неверный ObjectId")
        return PyObjectId(value)

    @validator("bookmarked_at")
    def validate_bookmarked_at(cls, value):
        if value > datetime.now():
            raise ValueError("Дата создания не может быть изменена в будущем")
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class UserBookmarkResponse(BaseModel):
    id: str
    movie_id: str
    user_id: str
    bookmarked_at: datetime
