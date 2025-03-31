from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)


class Nginx(BaseSettings):
    """Настройки Nginx."""

    host: str
    dsn: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="NGINX_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных."""

        self.dsn = f"http://{self.host}"


class KafkaSettings(BaseSettings):
    """Настройки Kafka."""

    host: str
    port: int
    dsn: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_prefix="KAFKA_")

    def model_post_init(self, __context):
        """Формируем DSN после загрузки переменных."""

        self.dsn = f"{self.host}:{self.port}"


nginx = Nginx()  # type: ignore
kafka_settings = KafkaSettings()  # type: ignore
