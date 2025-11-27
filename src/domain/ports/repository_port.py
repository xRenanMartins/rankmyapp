"""Port (interface) para repositório de pedidos."""

from abc import ABC, abstractmethod

from src.domain.entities.order import Order
from src.domain.value_objects.order_id import OrderId


class OrderRepositoryPort(ABC):
    """Interface para repositório de pedidos."""

    @abstractmethod
    async def save(self, order: Order) -> Order:
        """
        Salva ou atualiza um pedido.

        Args:
            order: Pedido a ser salvo

        Returns:
            Pedido salvo
        """
        pass

    @abstractmethod
    async def find_by_id(self, order_id: OrderId) -> Order | None:
        """
        Busca um pedido por ID.

        Args:
            order_id: ID do pedido

        Returns:
            Pedido encontrado ou None
        """
        pass
