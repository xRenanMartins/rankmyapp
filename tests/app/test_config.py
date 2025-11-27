"""Testes para configurações."""

import os
from unittest.mock import patch

from src.app.config import Settings, settings


def test_settings_defaults():
    """Testa valores padrão das configurações."""
    # Limpar variáveis de ambiente para testar defaults
    with patch.dict(os.environ, {}, clear=True):
        test_settings = Settings()

        assert test_settings.port == 8000
        assert test_settings.host == "0.0.0.0"
        assert test_settings.mongodb_url == "mongodb://localhost:27017"
        assert test_settings.mongodb_db_name == "order_db"
        assert test_settings.rabbitmq_url == "amqp://guest:guest@localhost:5672/"
        assert test_settings.rabbitmq_exchange == "order_events"
        assert test_settings.rabbitmq_routing_key == "order.status_updated"
        assert test_settings.log_level == "INFO"


def test_settings_instance():
    """Testa que settings é uma instância de Settings."""
    assert isinstance(settings, Settings)
    assert settings.port >= 0  # Validação básica
    assert settings.mongodb_db_name is not None
    assert settings.rabbitmq_exchange is not None
