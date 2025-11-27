"""Testes para entidade Order."""

import pytest

from src.domain.entities.order import Order
from src.domain.exceptions import InvalidStatusTransitionError
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus


def test_create_order():
    """Testa criação de pedido."""
    order = Order(
        order_id=OrderId("order-123"),
        customer_id="customer-123",
        items=[{"product_id": "prod-1", "quantity": 1}],
        total_amount=Money(100.0),
    )

    assert order.id == OrderId("order-123")
    assert order.customer_id == "customer-123"
    assert order.status == OrderStatus.PENDING
    assert order.total_amount.amount == 100.0


def test_update_status_valid_transition():
    """Testa atualização de status com transição válida."""
    order = Order(
        order_id=OrderId("order-123"),
        customer_id="customer-123",
        items=[],
        total_amount=Money(100.0),
        status=OrderStatus.PENDING,
    )

    old_status = order.update_status(OrderStatus.CONFIRMED)

    assert order.status == OrderStatus.CONFIRMED
    assert old_status == OrderStatus.PENDING


def test_update_status_invalid_transition():
    """Testa atualização de status com transição inválida."""
    order = Order(
        order_id=OrderId("order-123"),
        customer_id="customer-123",
        items=[],
        total_amount=Money(100.0),
        status=OrderStatus.PENDING,
    )

    with pytest.raises(InvalidStatusTransitionError):
        order.update_status(OrderStatus.DELIVERED)


def test_update_status_same_status():
    """Testa atualização para o mesmo status."""
    order = Order(
        order_id=OrderId("order-123"),
        customer_id="customer-123",
        items=[],
        total_amount=Money(100.0),
        status=OrderStatus.PENDING,
    )

    old_status = order.update_status(OrderStatus.PENDING)

    assert order.status == OrderStatus.PENDING
    assert old_status == OrderStatus.PENDING


def test_to_dict():
    """Testa conversão para dicionário."""
    order = Order(
        order_id=OrderId("order-123"),
        customer_id="customer-123",
        items=[{"product_id": "prod-1"}],
        total_amount=Money(100.0),
        status=OrderStatus.PENDING,
    )

    order_dict = order.to_dict()

    assert order_dict["id"] == "order-123"
    assert order_dict["customer_id"] == "customer-123"
    assert order_dict["status"] == "pending"
    assert order_dict["total_amount"]["amount"] == 100.0
