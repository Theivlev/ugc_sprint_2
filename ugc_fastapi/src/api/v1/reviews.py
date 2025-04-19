from typing import List, Tuple
from uuid import UUID

from pymongo.errors import DuplicateKeyError
from src.crud.base import BaseMongoCRUD
from src.models.review import UserReviews
from src.services.reviews import get_reviews_service
from src.shemas.user_reviews import UserReviewCreateDTO, UserReviewResponse
from src.utils.check_review import validate_review_exists
from src.shemas.pagination import PaginationLimits

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserReviewCreateDTO],
    summary="Получение списка рецензий",
    description="Возвращает список рецензий",
)
async def get_reviews_films(
    user_id: str,
    pagination: Tuple[int, int] = Depends(PaginationLimits.get_pagination_params),
    service: BaseMongoCRUD = Depends(get_reviews_service),
):
    """
    Получить список рецензий.
    """
    page_number, page_size = pagination
    filter_ = {"user_id": UUID(user_id)}
    reviews = await service.find(filter_, page_number, page_size)
    return [
        UserReviewResponse(
            id=str(review.id),
            movie_id=str(review.movie_id),
            user_id=str(review.user_id),
            reviewed_at=review.reviewed_at,
            review_text=review.review_text,
        )
        for review in reviews
    ]


@router.get(
    "/{review_id}",
    response_model=UserReviewCreateDTO,
    summary="Получение рецензии",
    description="Возвращает рецензию",
)
async def get_review_films(
    review_id: str,
    service: BaseMongoCRUD = Depends(get_reviews_service),
):
    """
    Получить рецензию.
    """
    review = await service.get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Рецензия не найдена")
    return UserReviewResponse(
        id=str(review.id),
        movie_id=str(review.movie_id),
        user_id=str(review.user_id),
        reviewed_at=review.reviewed_at,
        review_text=review.review_text,
    )


@router.post(
    "/",
    response_model=None,
    summary="Добавление рецензии",
    description="Добавляет рецензию",
)
async def add_reviews_films(
    review_data: UserReviewCreateDTO,
    service: BaseMongoCRUD = Depends(get_reviews_service),
):
    try:
        new_review = await service.create(review_data.model_dump(by_alias=True))
        return new_review
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Рецензия уже существует")


@router.delete(
    "/{review_id}",
    response_model=dict,
    summary="Удаление рецензии",
    description="Удаляет рецензию",
)
async def remove_review(
    review: UserReviews = Depends(validate_review_exists),
    service: BaseMongoCRUD = Depends(get_reviews_service),
):
    success = await service.delete(str(review.id))
    if not success:
        raise HTTPException(status_code=404, detail="Рецензия не найдена")
    return {"message": "Рецензия успешно удалена"}


@router.put(
    "/{review_id}",
    response_model=dict,
    summary="Обновление рецензии",
    description="Обновляет рецензию",
)
async def update_review(
    review_text: str,
    review: UserReviews = Depends(validate_review_exists),
    service: BaseMongoCRUD = Depends(get_reviews_service),
):
    data = {"review_text": review_text}
    success = await service.update(str(review.id), data)
    if not success:
        raise HTTPException(status_code=404, detail="Рецензия не найдена")
    return {"message": "Рецензия успешно обновлена"}
