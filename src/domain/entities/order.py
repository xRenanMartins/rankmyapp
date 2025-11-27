"""Entidade Order - representa um pedido no domínio."""

from datetime import datetime
from typing import Any

from src.domain.exceptions import InvalidStatusTransitionError
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus


class Order:
    """Entidade que representa um pedido."""

    def __init__(
        self,
        order_id: OrderId,
        customer_id: str,
        items: list[dict[str, Any]],
        total_amount: Money,
        status: OrderStatus = OrderStatus.PENDING,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """
        Inicializa um pedido.

        Args:
            order_id: Identificador único do pedido
            customer_id: ID do cliente
            items: Lista de itens do pedido
            total_amount: Valor total do pedido
            status: Status inicial (padrão: PENDING)
            created_at: Data de criação
            updated_at: Data de atualização
        """
        self._id = order_id
        self._customer_id = customer_id
        self._items = items
        self._total_amount = total_amount
        self._status = status
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()

    @property
    def id(self) -> OrderId:
        """Retorna o ID do pedido."""
        return self._id

    @property
    def customer_id(self) -> str:
        """Retorna o ID do cliente."""
        return self._customer_id

    @property
    def items(self) -> list[dict[str, Any]]:
        """Retorna os itens do pedido."""
        return self._items.copy()

    @property
    def total_amount(self) -> Money:
        """Retorna o valor total do pedido."""
        return self._total_amount

    @property
    def status(self) -> OrderStatus:
        """Retorna o status atual do pedido."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Retorna a data de criação."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Retorna a data de atualização."""
        return self._updated_at

    def update_status(self, new_status: OrderStatus) -> OrderStatus:
        """
        Atualiza o status do pedido seguindo as regras de negócio.

        Args:
            new_status: Novo status desejado

        Returns:
            Status anterior (para eventos)

        Raises:
            InvalidStatusTransitionError: Se a transição não é válida
        """
        if self._status == new_status:
            return self._status

        if not self._status.can_transition_to(new_status):
            raise InvalidStatusTransitionError(
                f"Não é possível transicionar de {self._status.value} para {new_status.value}"
            )

        old_status = self._status
        self._status = new_status
        self._updated_at = datetime.utcnow()

        return old_status

    def to_dict(self) -> dict[str, Any]:
        """
        Converte a entidade para dicionário.

        Returns:
            Dicionário com os dados do pedido
        """
        return {
            "id": self._id,
            "customer_id": self._customer_id,
            "items": self._items,
            "total_amount": {
                "amount": float(self._total_amount.amount),
                "currency": self._total_amount.currency,
            },
            "status": self._status.value,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }
