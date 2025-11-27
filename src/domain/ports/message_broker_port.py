"""Port (interface) para broker de mensagens."""

from abc import ABC, abstractmethod


class MessageBrokerPort(ABC):
    """Interface para publicação de eventos."""

    @abstractmethod
    async def publish_order_status_updated(
        self, order_id: str, old_status: str, new_status: str
    ) -> None:
        """
        Publica evento de atualização de status do pedido.

        Args:
            order_id: ID do pedido
            old_status: Status anterior
            new_status: Novo status
        """
        pass
