"""Caso de uso para obter um pedido por ID."""

import structlog

from src.domain.entities.order import Order
from src.domain.exceptions import OrderNotFoundError
from src.domain.ports.repository_port import OrderRepositoryPort
from src.domain.value_objects.order_id import OrderId

logger = structlog.get_logger()


class GetOrderUseCase:
    """Caso de uso para obter um pedido por ID."""

    def __init__(self, repository: OrderRepositoryPort) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repository: Repositório de pedidos
        """
        self._repository = repository

    async def execute(self, order_id: OrderId) -> Order:
        """
        Obtém um pedido por ID.

        Args:
            order_id: ID do pedido

        Returns:
            Pedido encontrado

        Raises:
            OrderNotFoundError: Se o pedido não for encontrado
        """
        logger.info("Buscando pedido", order_id=str(order_id))

        order = await self._repository.find_by_id(order_id)

        if not order:
            logger.warning("Pedido não encontrado", order_id=str(order_id))
            raise OrderNotFoundError(f"Pedido {order_id} não encontrado")

        logger.info("Pedido encontrado", order_id=str(order_id))

        return order
