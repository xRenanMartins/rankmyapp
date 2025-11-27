"""Schemas Pydantic para entrada/saída da API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class MoneySchema(BaseModel):
    """Schema para valor monetário."""

    amount: float = Field(..., description="Valor numérico")
    currency: str = Field(default="BRL", description="Moeda")


class OrderItemSchema(BaseModel):
    """Schema para item do pedido."""

    product_id: str = Field(..., description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade")
    price: float = Field(..., gt=0, description="Preço unitário")


class CreateOrderRequest(BaseModel):
    """Schema para criação de pedido."""

    customer_id: str = Field(..., description="ID do cliente")
    items: list[dict[str, Any]] = Field(..., description="Lista de itens do pedido")
    total_amount: float = Field(..., gt=0, description="Valor total do pedido")


class UpdateOrderStatusRequest(BaseModel):
    """Schema para atualização de status."""

    status: str = Field(..., description="Novo status do pedido")


class OrderResponse(BaseModel):
    """Schema de resposta do pedido."""

    id: str = Field(..., description="ID do pedido")
    customer_id: str = Field(..., description="ID do cliente")
    items: list[dict[str, Any]] = Field(..., description="Lista de itens")
    total_amount: MoneySchema = Field(..., description="Valor total")
    status: str = Field(..., description="Status do pedido")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")

    class Config:
        """Configuração do Pydantic."""

        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "customer_id": "customer-123",
                "items": [{"product_id": "prod-1", "quantity": 2, "price": 50.0}],
                "total_amount": {"amount": 100.0, "currency": "BRL"},
                "status": "pending",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00",
            }
        }
