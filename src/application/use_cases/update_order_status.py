"""Caso de uso para atualizar o status de um pedido."""

import structlog

from src.domain.entities.order import Order
from src.domain.exceptions import OrderNotFoundError
from src.domain.ports.message_broker_port import MessageBrokerPort
from src.domain.ports.repository_port import OrderRepositoryPort
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus

logger = structlog.get_logger()


class UpdateOrderStatusUseCase:
    """Caso de uso para atualizar o status de um pedido."""

    def __init__(
        self,
        repository: OrderRepositoryPort,
        message_broker: MessageBrokerPort,
    ) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repository: Repositório de pedidos
            message_broker: Broker de mensagens para publicar eventos
        """
        self._repository = repository
        self._message_broker = message_broker

    async def execute(self, order_id: OrderId, new_status: OrderStatus) -> Order:
        """
        Atualiza o status de um pedido e publica evento.

        Args:
            order_id: ID do pedido
            new_status: Novo status

        Returns:
            Pedido atualizado

        Raises:
            OrderNotFoundError: Se o pedido não for encontrado
            InvalidStatusTransitionError: Se a transição de status for inválida
        """
        logger.info(
            "Atualizando status do pedido",
            order_id=str(order_id),
            new_status=new_status.value,
        )

        order = await self._repository.find_by_id(order_id)

        if not order:
            logger.warning("Pedido não encontrado", order_id=str(order_id))
            raise OrderNotFoundError(f"Pedido {order_id} não encontrado")

        old_status = order.update_status(new_status)
        updated_order = await self._repository.save(order)

        # Publica evento de mudança de status
        await self._message_broker.publish_order_status_updated(
            order_id=str(order_id),
            old_status=old_status.value,
            new_status=new_status.value,
        )

        logger.info(
            "Status do pedido atualizado com sucesso",
            order_id=str(order_id),
            old_status=old_status.value,
            new_status=new_status.value,
        )

        return updated_order
