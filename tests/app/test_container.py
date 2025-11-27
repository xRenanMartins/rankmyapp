"""Testes para container de dependency injection."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.adapters.messaging.rabbitmq_publisher import RabbitMQPublisher
from src.adapters.persistence.mongo_order_repository import MongoOrderRepository
from src.app.container import Container


@pytest.fixture
def container():
    """Cria instância do container para testes."""
    return Container()


@pytest.mark.asyncio
async def test_container_initialization(container):
    """Testa inicialização do container."""
    with (
        patch("src.app.container.AsyncIOMotorClient") as mock_mongo,
        patch("src.app.container.connect_robust") as mock_rabbitmq,
    ):

        mock_db = MagicMock()
        mock_mongo.return_value.__getitem__.return_value = mock_db

        mock_connection = AsyncMock()
        mock_rabbitmq.return_value = mock_connection

        await container.initialize()

        assert container._repository is not None
        assert container._message_broker is not None
        assert isinstance(container._repository, MongoOrderRepository)
        assert isinstance(container._message_broker, RabbitMQPublisher)


@pytest.mark.asyncio
async def test_container_shutdown(container):
    """Testa shutdown do container."""
    container._mongo_client = MagicMock()
    container._rabbitmq_connection = AsyncMock()

    await container.shutdown()

    container._mongo_client.close.assert_called_once()
    assert container._rabbitmq_connection.close.called


def test_get_create_order_use_case(container):
    """Testa get_create_order_use_case."""
    container._repository = MagicMock()

    use_case = container.get_create_order_use_case()

    assert use_case is not None


def test_get_create_order_use_case_not_initialized(container):
    """Testa get_create_order_use_case sem inicialização."""
    container._repository = None

    with pytest.raises(RuntimeError, match="não inicializado"):
        container.get_create_order_use_case()


def test_get_get_order_use_case(container):
    """Testa get_get_order_use_case."""
    container._repository = MagicMock()

    use_case = container.get_get_order_use_case()

    assert use_case is not None


def test_get_update_order_status_use_case(container):
    """Testa get_update_order_status_use_case."""
    container._repository = MagicMock()
    container._message_broker = MagicMock()

    use_case = container.get_update_order_status_use_case()

    assert use_case is not None


def test_get_update_order_status_use_case_not_initialized(container):
    """Testa get_update_order_status_use_case sem inicialização."""
    container._repository = None
    container._message_broker = None

    with pytest.raises(RuntimeError, match="não inicializado"):
        container.get_update_order_status_use_case()
