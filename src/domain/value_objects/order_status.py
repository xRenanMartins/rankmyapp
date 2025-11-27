"""Value object para status do pedido."""

from enum import Enum


class OrderStatus(str, Enum):
    """Status possíveis de um pedido."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    @classmethod
    def get_valid_transitions(cls, current_status: "OrderStatus") -> list["OrderStatus"]:
        """
        Retorna as transições válidas a partir de um status.

        Args:
            current_status: Status atual do pedido

        Returns:
            Lista de status válidos para transição
        """
        transitions = {
            cls.PENDING: [cls.CONFIRMED, cls.CANCELLED],
            cls.CONFIRMED: [cls.PROCESSING, cls.CANCELLED],
            cls.PROCESSING: [cls.SHIPPED, cls.CANCELLED],
            cls.SHIPPED: [cls.DELIVERED],
            cls.DELIVERED: [],
            cls.CANCELLED: [],
        }
        return transitions.get(current_status, [])

    def can_transition_to(self, new_status: "OrderStatus") -> bool:
        """
        Verifica se é possível transicionar para um novo status.

        Args:
            new_status: Novo status desejado

        Returns:
            True se a transição é válida, False caso contrário
        """
        return new_status in self.get_valid_transitions(self)
