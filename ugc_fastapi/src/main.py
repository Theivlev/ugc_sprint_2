from contextlib import asynccontextmanager

from fastapi.responses import ORJSONResponse

from src.core.config import project_settings

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield

    finally:
        app.state.fast_server_task.cancel()


app = FastAPI(
    title=project_settings.project_name,
    docs_url="/auth/openapi",
    openapi_url="/auth/openapi.json",
    default_response_class=ORJSONResponse,
    summary=project_settings.project_summary,
    version=project_settings.project_version,
    terms_of_service=project_settings.project_terms_of_service,
    #openapi_tags=project_settings.project_tags,
    lifespan=lifespan,
)
