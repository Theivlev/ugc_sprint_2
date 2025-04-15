from datetime import datetime

from mixin import ObjectIdMixin, PyObjectId
from pydantic import Field


class UserReviews(ObjectIdMixin):
    """Модель для коллекции 'user_reviews'."""

    movie_id: PyObjectId
    user_id: PyObjectId
    review_text: str
    rating: int = Field(..., ge=1, le=10)
    reviewed_at: datetime
