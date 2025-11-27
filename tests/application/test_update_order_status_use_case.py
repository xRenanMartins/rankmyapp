"""Testes para UpdateOrderStatusUseCase."""

from unittest.mock import AsyncMock

import pytest

from src.application.use_cases.update_order_status import UpdateOrderStatusUseCase
from src.domain.entities.order import Order
from src.domain.exceptions import InvalidStatusTransitionError, OrderNotFoundError
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus


@pytest.mark.asyncio
async def test_update_order_status_success(mock_repository, mock_message_broker):
    """Testa atualização de status com sucesso."""
    # Arrange
    use_case = UpdateOrderStatusUseCase(mock_repository, mock_message_broker)
    order_id = OrderId("order-123")
    order = Order(
        order_id=order_id,
        customer_id="customer-123",
        items=[],
        total_amount=Money(100.0),
        status=OrderStatus.PENDING,
    )
    mock_repository.find_by_id = AsyncMock(return_value=order)
    mock_repository.save = AsyncMock(return_value=order)
    mock_message_broker.publish_order_status_updated = AsyncMock()

    # Act
    result = await use_case.execute(order_id, OrderStatus.CONFIRMED)

    # Assert
    assert result.status == OrderStatus.CONFIRMED
    mock_repository.find_by_id.assert_called_once_with(order_id)
    mock_repository.save.assert_called_once()
    mock_message_broker.publish_order_status_updated.assert_called_once_with(
        order_id=str(order_id),
        old_status="pending",
        new_status="confirmed",
    )


@pytest.mark.asyncio
async def test_update_order_status_not_found(mock_repository, mock_message_broker):
    """Testa atualização de status de pedido inexistente."""
    # Arrange
    use_case = UpdateOrderStatusUseCase(mock_repository, mock_message_broker)
    order_id = OrderId("order-123")
    mock_repository.find_by_id = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(OrderNotFoundError):
        await use_case.execute(order_id, OrderStatus.CONFIRMED)

    mock_message_broker.publish_order_status_updated.assert_not_called()


@pytest.mark.asyncio
async def test_update_order_status_invalid_transition(mock_repository, mock_message_broker):
    """Testa atualização de status com transição inválida."""
    # Arrange
    use_case = UpdateOrderStatusUseCase(mock_repository, mock_message_broker)
    order_id = OrderId("order-123")
    order = Order(
        order_id=order_id,
        customer_id="customer-123",
        items=[],
        total_amount=Money(100.0),
        status=OrderStatus.PENDING,
    )
    mock_repository.find_by_id = AsyncMock(return_value=order)

    # Act & Assert
    with pytest.raises(InvalidStatusTransitionError):
        await use_case.execute(order_id, OrderStatus.DELIVERED)

    mock_message_broker.publish_order_status_updated.assert_not_called()
