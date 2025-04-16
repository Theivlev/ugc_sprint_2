from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import project_settings

from src.api.v1.bookmarks import router as bookmarks_router



@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.client = AsyncIOMotorClient(str(project_settings.mongo_dsn))
    app.state.db = app.state.client[project_settings.mongo_db]
    try:
        yield
    finally:
        await app.state.client.close()

app = FastAPI(
    title=project_settings.project_name,
    docs_url="/openapi",
    openapi_url="/openapi.json",
    default_response_class=ORJSONResponse,
    summary=project_settings.project_summary,
    version=project_settings.project_version,
    terms_of_service=project_settings.project_terms_of_service,
    # openapi_tags=project_settings.project_tags,
    lifespan=lifespan,
)

app.include_router(bookmarks_router, prefix="/bookmarks", tags=["Bookmarks"])