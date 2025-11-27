"""Testes para CreateOrderUseCase."""

from unittest.mock import AsyncMock

import pytest

from src.application.use_cases.create_order import CreateOrderUseCase
from src.domain.entities.order import Order
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus


@pytest.mark.asyncio
async def test_create_order_success(mock_repository):
    """Testa criação de pedido com sucesso."""
    # Arrange
    use_case = CreateOrderUseCase(mock_repository)
    customer_id = "customer-123"
    items = [{"product_id": "prod-1", "quantity": 2}]
    total_amount = 100.0

    # Mock do repositório retornando o pedido salvo
    saved_order = Order(
        order_id=OrderId("order-123"),
        customer_id=customer_id,
        items=items,
        total_amount=Money(100.0),
    )
    mock_repository.save = AsyncMock(return_value=saved_order)

    # Act
    result = await use_case.execute(customer_id, items, total_amount)

    # Assert
    assert result.customer_id == customer_id
    assert result.status == OrderStatus.PENDING
    mock_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_order_generates_uuid(mock_repository):
    """Testa que um UUID é gerado para o pedido."""
    # Arrange
    use_case = CreateOrderUseCase(mock_repository)
    saved_order = Order(
        order_id=OrderId("order-123"),
        customer_id="customer-123",
        items=[],
        total_amount=Money(100.0),
    )
    mock_repository.save = AsyncMock(return_value=saved_order)

    # Act
    result = await use_case.execute("customer-123", [], 100.0)

    # Assert
    assert result is not None
    # Verifica que save foi chamado com um Order que tem ID
    call_args = mock_repository.save.call_args[0][0]
    assert call_args.id is not None
