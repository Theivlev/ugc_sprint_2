import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    """Настройки RabbitMQ."""

    host: str
    user: str
    password: str
    port: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="RABBITMQ_")


rabbit_settings = RabbitMQSettings()  # type: ignore

# Настройки логирования
LOGGER_FORMAT = "%(asctime)s [%(levelname)s] - %(message)s"
LOGGER_SETTINGS = {
    "level": logging.INFO,
    "format": LOGGER_FORMAT,
    "handlers": [
        logging.StreamHandler(),
    ],
}
logging.basicConfig(**LOGGER_SETTINGS)
