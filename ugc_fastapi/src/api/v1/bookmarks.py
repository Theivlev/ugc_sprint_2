from typing import List, Tuple
from uuid import UUID

from pymongo.errors import DuplicateKeyError
from src.crud.base import BaseMongoCRUD
from src.models.bookmark import UserBookmarks
from src.services.bookmarks import get_bookmark_service
from src.shemas.user_bookmarks import UserBookmarkCreateDTO, UserBookmarkResponse
from src.utils.check_bookmark import validate_bookmark_exists
from src.paginations.pagination import PaginationLimits

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserBookmarkResponse],
    summary="Получение списка фильмов в закладках пользователя",
    description="Возвращает список фильмов в закладках пользователя",
)
async def get_bookmarks_films(
    user_id: str,
    pagination: Tuple[int, int] = Depends(PaginationLimits.get_pagination_params),
    service: BaseMongoCRUD = Depends(get_bookmark_service),
):
    """
    Получить список фильмов в закладках пользователя.
    """
    try:
        uuid_obj = UUID(user_id)
        page_number, page_size = pagination
        filter_ = {"user_id": uuid_obj}

        bookmarks = await service.find(filter_, page_number, page_size)

        return [
            UserBookmarkResponse.from_bookmark(bookmark)
            for bookmark in bookmarks
        ]
    except HTTPException as e:
        raise e
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат user_id. Ожидается UUID.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


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
    try:
        success = await service.delete(str(bookmark.id))
        if not success:
            raise HTTPException(status_code=404, detail="Закладка не найдена")
        return {"message": "Закладка успешно удалена"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")