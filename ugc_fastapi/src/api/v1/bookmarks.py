from typing import List
from uuid import UUID

from pymongo.errors import DuplicateKeyError
from src.crud.base import BaseMongoCRUD
from src.models.bookmark import UserBookmarks
from src.services.bookmarks import get_bookmark_service
from src.shemas.user_bookmarks import UserBookmarkCreateDTO, UserBookmarkResponse
from src.utils.check_bookmark import validate_bookmark_exists

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserBookmarkResponse],
    summary="Получение списка фильмов в закладках пользователя",
    description="Возвращает список фильмов в закладках пользователя",
)
async def get_bookmarks_films(
    user_id: str,
    page_number: int = Query(0, ge=0, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    service: BaseMongoCRUD = Depends(get_bookmark_service),
):
    """
    Получить список фильмов в закладках пользователя.
    """
    filter_ = {"user_id": UUID(user_id)}
    bookmarks = await service.find(filter_, page_number, page_size)
    return [
        UserBookmarkResponse(
            id=str(bookmark.id),
            movie_id=str(bookmark.movie_id),
            user_id=str(bookmark.user_id),
            bookmarked_at=bookmark.bookmarked_at,
        )
        for bookmark in bookmarks
    ]


@router.post(
    "/",
    response_model=None,
    summary="Добавление закладки",
    description="Добавляет фильм в закладки пользователя",
)
async def add_bookmarks_films(
    bookmark_data: UserBookmarkCreateDTO,
    service: BaseMongoCRUD = Depends(get_bookmark_service),
):
    try:
        new_bookmark = await service.create(bookmark_data.model_dump(by_alias=True))
        return new_bookmark
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Закладка уже существует")


@router.delete(
    "/{bookmark_id}",
    response_model=dict,
    summary="Удаление закладки",
    description="Удаляет фильм из закладок пользователя",
)
async def remove_bookmark(
    bookmark: UserBookmarks = Depends(validate_bookmark_exists),
    service: BaseMongoCRUD = Depends(get_bookmark_service),
):
    success = await service.delete(str(bookmark.id))
    if not success:
        raise HTTPException(status_code=404, detail="Закладка не найдена")
    return {"message": "Закладка успешно удалена"}
