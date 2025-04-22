from contextlib import asynccontextmanager

from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from src.api.routers import main_router
from src.core.config import project_settings
from src.db.mongo import init_db

from fastapi import FastAPI, Request, status  # noqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = AsyncIOMotorClient(str(project_settings.mongo_dsn))
    app.state.db = app.state.client[project_settings.mongo_db]

    await init_db(app.state.db)
    try:
        yield
    finally:
        await app.state.client.close()


app = FastAPI(
    title=project_settings.project_auth_name,
    docs_url="/social/openapi",
    openapi_url="/social/openapi.json",
    default_response_class=ORJSONResponse,
    summary=project_settings.project_auth_summary,
    version=project_settings.project_auth_version,
    terms_of_service=project_settings.project_auth_terms_of_service,
    openapi_tags=project_settings.project_auth_tags,
    lifespan=lifespan,
)

app.include_router(main_router)


# @app.middleware("http")
# async def before_request(request: Request, call_next):
#     response = await call_next(request)
#     request_id = request.headers.get("X-Request-Id")
#     if not request_id:
#         return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "X-Request-Id is required"})
#     return response
