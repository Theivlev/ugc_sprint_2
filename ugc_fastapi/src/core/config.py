from logging import config as logging_config

from pydantic import Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class Settings(BaseSettings):
    """Настраивает класс для чтения переменных окружения.."""

    project_auth_name: str
    project_auth_summary: str
    project_auth_version: str
    project_auth_terms_of_service: str
    project_auth_tags: list = Field(
        default=[
            {
                "name": "bookmarks",
                "description": "Operations with bookmarks.",
            },
            {
                "name": "likes",
                "description": "Operations with likes.",
            },
            {
                "name": "reviews",
                "description": "Operations with reviews.",
            },
        ]
    )

    mongo_dsn: MongoDsn
    mongo_db: str

    auth_grpc_host: str
    auth_grpc_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


project_settings = Settings()
