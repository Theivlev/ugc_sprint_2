from fastapi import HTTPException
from src.crud.base import BaseMongoCRUD
from fastapi import Depends
from src.services.bookmarks import get_crud_service

async def validate_bookmark_exists(bookmark_id: str, service: BaseMongoCRUD = Depends(get_crud_service)):
    bookmark = await service.get(bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Закладка не найдена")
    return bookmark
