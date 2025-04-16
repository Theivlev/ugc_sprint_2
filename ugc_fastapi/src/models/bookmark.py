from datetime import datetime

from mixin import ObjectIdMixin, PyObjectId


class UserBookmarks(ObjectIdMixin):
    """Модель для коллекции 'user_bookmarks'."""

    movie_id: PyObjectId
    user_id: PyObjectId
    bookmarked_at: datetime
