from datetime import datetime

from mixin import ObjectIdMixin, PyObjectId
from pydantic import Field


class UserLike(ObjectIdMixin):
    """Модель для коллекции 'user_likes'."""

    movie_id: PyObjectId
    user_id: PyObjectId
    liked_at: datetime
