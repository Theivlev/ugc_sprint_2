from typing import List
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from src.shemas.user_bookmarks import UserBookmarkCreateDTO, UserBookmarkUpdateDTO  # noqa
from src.crud.base import BaseMongoCRUD
from src.models.bookmark import UserBookmarks
from src.services.bookmarks import get_user_bookmark_service

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


@router.get("/", response_model=List[UserBookmarks])
async def get_bookmarks_films(
    user_id: str,
    page_number: int = Query(0, ge=0, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    service: BaseMongoCRUD = Depends(get_user_bookmark_service),
):
    """
    Получить список фильмов в закладках пользователя.
    """
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Некорректный ID пользователя")

        filter_ = {"user_id": ObjectId(user_id)}
        bookmarks = await service.find(filter_, page_number, page_size)
        return bookmarks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


@router.post("/", response_model=UserBookmarks)
async def add_bookmarks_films(
    bookmark_data: UserBookmarkCreateDTO,
    service: BaseMongoCRUD = Depends(get_user_bookmark_service),
):
    """
    Добавить фильм в закладки пользователя.
    """
    try:
        if not ObjectId.is_valid(bookmark_data.movie_id) or not ObjectId.is_valid(bookmark_data.user_id):
            raise HTTPException(status_code=400, detail="Некорректный ID фильма или пользователя")

        new_bookmark = await service.create(bookmark_data)
        return new_bookmark
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Закладка уже существует")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


@router.delete("/{bookmark_id}", response_model=dict)
async def remove_bookmark(
    bookmark_id: str,
    service: BaseMongoCRUD = Depends(get_user_bookmark_service),
):
    """
    Удалить фильм из закладок пользователя.
    """
    try:
        if not ObjectId.is_valid(bookmark_id):
            raise HTTPException(status_code=400, detail="Некорректный ID закладки")

        is_deleted = await service.delete(bookmark_id)
        if not is_deleted:
            raise HTTPException(status_code=404, detail="Закладка не найдена")

        return {"message": "Закладка успешно удалена"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
