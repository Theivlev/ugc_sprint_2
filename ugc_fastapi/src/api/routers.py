from src.api.v1 import bookmarks_router

from fastapi import APIRouter

API_V1: str = "/api/v1"
main_router = APIRouter()
main_router.include_router(bookmarks_router, prefix=f"{API_V1}/bookmarks", tags=["bookmarks"])
