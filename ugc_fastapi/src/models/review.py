from datetime import datetime

from mixin import ObjectIdMixin, PyObjectId
from pydantic import Field


class UserReviews(ObjectIdMixin):
    """Модель для коллекции 'user_reviews'."""

    movie_id: PyObjectId
    user_id: PyObjectId
    review_text: str
    reviewed_at: datetime
