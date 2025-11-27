"""Caso de uso para criar um pedido."""

import uuid
from typing import Any

import structlog

from src.domain.entities.order import Order
from src.domain.ports.repository_port import OrderRepositoryPort
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus

logger = structlog.get_logger()


class CreateOrderUseCase:
    """Caso de uso para criar um novo pedido."""

    def __init__(self, repository: OrderRepositoryPort) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repository: Repositório de pedidos
        """
        self._repository = repository

    async def execute(
        self, customer_id: str, items: list[dict[str, Any]], total_amount: float
    ) -> Order:
        """
        Cria um novo pedido.

        Args:
            customer_id: ID do cliente
            items: Lista de itens do pedido
            total_amount: Valor total do pedido

        Returns:
            Pedido criado
        """
        logger.info(
            "Criando pedido",
            customer_id=customer_id,
            items_count=len(items),
            total_amount=total_amount,
        )

        order_id = OrderId(str(uuid.uuid4()))
        money = Money(total_amount)
        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            items=items,
            total_amount=money,
            status=OrderStatus.PENDING,
        )

        saved_order = await self._repository.save(order)

        logger.info("Pedido criado com sucesso", order_id=str(saved_order.id))

        return saved_order
