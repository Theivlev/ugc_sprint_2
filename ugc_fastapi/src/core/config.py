from logging import config as logging_config

from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class Settings(BaseSettings):
    """Настраивает класс для чтения переменных окружения.."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    project_name: str
    project_summary: str
    project_version: str
    project_terms_of_service: str

    mongo_dsn: MongoDsn
    mongo_db: str

    auth_grpc_host: str
    auth_grpc_port: int


project_settings = Settings()
