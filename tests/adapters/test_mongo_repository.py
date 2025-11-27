"""Testes para MongoOrderRepository."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.adapters.persistence.mongo_order_repository import MongoOrderRepository
from src.domain.entities.order import Order
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus


@pytest.fixture
def mock_database():
    """Cria mock do banco de dados MongoDB."""
    database = MagicMock()
    collection = AsyncMock()
    database.__getitem__ = MagicMock(return_value=collection)
    return database, collection


@pytest.mark.asyncio
async def test_save_order(mock_database):
    """Testa salvamento de pedido."""
    # Arrange
    database, collection = mock_database
    repository = MongoOrderRepository(database)
    order = Order(
        order_id=OrderId("order-123"),
        customer_id="customer-123",
        items=[{"product_id": "prod-1"}],
        total_amount=Money(100.0),
        status=OrderStatus.PENDING,
    )

    # Act
    result = await repository.save(order)

    # Assert
    assert result == order
    collection.update_one.assert_called_once()


@pytest.mark.asyncio
async def test_find_by_id_found(mock_database):
    """Testa busca de pedido existente."""
    # Arrange
    database, collection = mock_database
    repository = MongoOrderRepository(database)
    order_id = OrderId("order-123")
    document = {
        "id": "order-123",
        "customer_id": "customer-123",
        "items": [{"product_id": "prod-1"}],
        "total_amount": {"amount": 100.0, "currency": "BRL"},
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    collection.find_one = AsyncMock(return_value=document)

    # Act
    result = await repository.find_by_id(order_id)

    # Assert
    assert result is not None
    assert result.id == order_id
    collection.find_one.assert_called_once_with({"id": order_id})


@pytest.mark.asyncio
async def test_find_by_id_not_found(mock_database):
    """Testa busca de pedido inexistente."""
    # Arrange
    database, collection = mock_database
    repository = MongoOrderRepository(database)
    order_id = OrderId("order-123")
    collection.find_one = AsyncMock(return_value=None)

    # Act
    result = await repository.find_by_id(order_id)

    # Assert
    assert result is None
