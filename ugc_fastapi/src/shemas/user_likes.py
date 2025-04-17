from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field, validator
from src.models.dto import AbstractDTO


class UserLikeCreateDTO(AbstractDTO):
    movie_id: UUID
    user_id: UUID
    rating: int
    liked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @validator("rating")
    def validate_rating(cls, value):
        if value < 1:
            raise ValueError("Оценка рейтинга должна быть больше 0!")
        if value > 10:
            raise ValueError("Оценка рейтинга должна быть меньше 10!")
        return value

    @validator("liked_at")
    def validate_liked_at(cls, value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        if value > datetime.now(timezone.utc):
            raise ValueError("Дата создания не может быть изменена в будущем")
        return value


class UserLikeResponse(BaseModel):
    id: str
    movie_id: str
    user_id: str
    liked_at: datetime
    rating: int

    @validator("liked_at")
    def ensure_timezone(cls, value):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
