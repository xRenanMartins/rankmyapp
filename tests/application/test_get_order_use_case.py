"""Testes para GetOrderUseCase."""

from unittest.mock import AsyncMock

import pytest

from src.application.use_cases.get_order import GetOrderUseCase
from src.domain.entities.order import Order
from src.domain.exceptions import OrderNotFoundError
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId


@pytest.mark.asyncio
async def test_get_order_success(mock_repository):
    """Testa busca de pedido com sucesso."""
    # Arrange
    use_case = GetOrderUseCase(mock_repository)
    order_id = OrderId("order-123")
    order = Order(
        order_id=order_id,
        customer_id="customer-123",
        items=[],
        total_amount=Money(100.0),
    )
    mock_repository.find_by_id = AsyncMock(return_value=order)

    # Act
    result = await use_case.execute(order_id)

    # Assert
    assert result.id == order_id
    mock_repository.find_by_id.assert_called_once_with(order_id)


@pytest.mark.asyncio
async def test_get_order_not_found(mock_repository):
    """Testa busca de pedido inexistente."""
    # Arrange
    use_case = GetOrderUseCase(mock_repository)
    order_id = OrderId("order-123")
    mock_repository.find_by_id = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(OrderNotFoundError):
        await use_case.execute(order_id)
