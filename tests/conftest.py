"""Configuração compartilhada para testes."""

from unittest.mock import AsyncMock

import pytest

from src.domain.entities.order import Order
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus


@pytest.fixture
def sample_order() -> Order:
    """Cria um pedido de exemplo para testes."""
    return Order(
        order_id=OrderId("test-order-123"),
        customer_id="customer-123",
        items=[{"product_id": "prod-1", "quantity": 2, "price": 50.0}],
        total_amount=Money(100.0),
        status=OrderStatus.PENDING,
    )


@pytest.fixture
def mock_repository() -> AsyncMock:
    """Cria um mock do repositório."""
    repository = AsyncMock()
    return repository


@pytest.fixture
def mock_message_broker() -> AsyncMock:
    """Cria um mock do message broker."""
    broker = AsyncMock()
    return broker
