"""Configurações da aplicação."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Servidor
    port: int = 8000
    host: str = "0.0.0.0"

    # MongoDB
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "order_db"

    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    rabbitmq_exchange: str = "order_events"
    rabbitmq_routing_key: str = "order.status_updated"

    # Logging
    log_level: str = "INFO"


settings = Settings()
