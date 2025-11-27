"""Testes para schemas Pydantic."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.adapters.http.schemas import (
    CreateOrderRequest,
    MoneySchema,
    OrderResponse,
    UpdateOrderStatusRequest,
)


def test_money_schema():
    """Testa MoneySchema."""
    schema = MoneySchema(amount=100.0, currency="BRL")

    assert schema.amount == 100.0
    assert schema.currency == "BRL"


def test_money_schema_default_currency():
    """Testa MoneySchema com moeda padrão."""
    schema = MoneySchema(amount=50.0)

    assert schema.amount == 50.0
    assert schema.currency == "BRL"


def test_create_order_request():
    """Testa CreateOrderRequest."""
    request = CreateOrderRequest(
        customer_id="customer-123",
        items=[{"product_id": "prod-1", "quantity": 2}],
        total_amount=100.0,
    )

    assert request.customer_id == "customer-123"
    assert len(request.items) == 1
    assert request.total_amount == 100.0


def test_create_order_request_validation():
    """Testa validação de CreateOrderRequest."""
    with pytest.raises(ValidationError):
        CreateOrderRequest(
            customer_id="customer-123",
            items=[],
            total_amount=-10.0,  # Valor negativo deve falhar
        )


def test_update_order_status_request():
    """Testa UpdateOrderStatusRequest."""
    request = UpdateOrderStatusRequest(status="confirmed")

    assert request.status == "confirmed"


def test_order_response():
    """Testa OrderResponse."""
    response = OrderResponse(
        id="order-123",
        customer_id="customer-123",
        items=[{"product_id": "prod-1"}],
        total_amount=MoneySchema(amount=100.0, currency="BRL"),
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    assert response.id == "order-123"
    assert response.customer_id == "customer-123"
    assert response.status == "pending"
    assert response.total_amount.amount == 100.0
