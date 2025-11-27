"""Testes para RabbitMQPublisher."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.adapters.messaging.rabbitmq_publisher import RabbitMQPublisher


@pytest.fixture
def mock_connection():
    """Cria mock da conexão RabbitMQ."""
    connection = MagicMock()
    channel = AsyncMock()
    exchange = AsyncMock()
    connection.channel = AsyncMock(return_value=channel)
    channel.declare_exchange = AsyncMock(return_value=exchange)
    return connection, exchange


@pytest.mark.asyncio
async def test_publish_order_status_updated(mock_connection):
    """Testa publicação de evento de atualização de status."""
    # Arrange
    connection, exchange = mock_connection
    publisher = RabbitMQPublisher(connection)
    await publisher.connect()

    # Act
    await publisher.publish_order_status_updated(
        order_id="order-123",
        old_status="pending",
        new_status="confirmed",
    )

    # Assert
    exchange.publish.assert_called_once()
    # Verifica que publish foi chamado (a estrutura exata pode variar)
    assert exchange.publish.called
