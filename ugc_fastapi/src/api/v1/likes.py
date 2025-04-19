from typing import List, Tuple
from uuid import UUID

from pymongo.errors import DuplicateKeyError
from src.crud.base import BaseMongoCRUD
from src.models.like import UserLikes
from src.services.likes import get_likes_service
from src.shemas.user_likes import UserLikeCreateDTO, UserLikeResponse
from src.utils.check_like import validate_like_exists
from src.paginations.pagination import PaginationLimits

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserLikeCreateDTO],
    summary="Получение списка лайков",
    description="Возвращает список лайков",
)
async def get_likes_films(
    user_id: str,
    pagination: Tuple[int, int] = Depends(PaginationLimits.get_pagination_params),
    service: BaseMongoCRUD = Depends(get_likes_service),
):
    """
    Получить список лайков.
    """
    page_number, page_size = pagination
    filter_ = {"user_id": UUID(user_id)}
    likes = await service.find(filter_, page_number, page_size)
    return [
        UserLikeResponse(
            id=str(like.id),
            movie_id=str(like.movie_id),
            user_id=str(like.user_id),
            liked_at=like.liked_at,
            rating=like.rating,
        )
        for like in likes
    ]


@router.get(
    "/{like_id}",
    response_model=UserLikeCreateDTO,
    summary="Получение лайка",
    description="Возвращает лайк",
)
async def get_like_films(
    like_id: str,
    service: BaseMongoCRUD = Depends(get_likes_service),
):
    """
    Получить лайк.
    """
    like = await service.get(like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Лайк не найден")
    return UserLikeResponse(
        id=str(like.id),
        movie_id=str(like.movie_id),
        user_id=str(like.user_id),
        liked_at=like.liked_at,
        rating=like.rating,
    )


@router.post(
    "/",
    response_model=None,
    summary="Добавление лайка",
    description="Добавляет лайк",
)
async def add_likes_films(
    like_data: UserLikeCreateDTO,
    service: BaseMongoCRUD = Depends(get_likes_service),
):
    try:
        new_like = await service.create(like_data.model_dump(by_alias=True))
        return new_like
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Лайк уже существует")


@router.delete(
    "/{like_id}",
    response_model=dict,
    summary="Удаление лайка",
    description="Удаляет лайк",
)
async def remove_like(
    like: UserLikes = Depends(validate_like_exists),
    service: BaseMongoCRUD = Depends(get_likes_service),
):
    success = await service.delete(str(like.id))
    if not success:
        raise HTTPException(status_code=404, detail="Лайк не найден")
    return {"message": "Лайк успешно удален"}


@router.put(
    "/{like_id}",
    response_model=dict,
    summary="Обновление лайка",
    description="Обновляет лайк",
)
async def update_like(
    rating: int = Query(ge=1, le=10, description="Оценка рейтинга"),
    like: UserLikes = Depends(validate_like_exists),
    service: BaseMongoCRUD = Depends(get_likes_service),
):
    data = {"rating": rating}
    success = await service.update(str(like.id), data)
    if not success:
        raise HTTPException(status_code=404, detail="Лайк не найден")
    return {"message": "Лайк успешно обновлен"}
