"""Adapter MongoDB para repositório de pedidos."""

from datetime import datetime
from typing import Any

import structlog
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from src.domain.entities.order import Order
from src.domain.ports.repository_port import OrderRepositoryPort
from src.domain.value_objects.money import Money
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus

logger = structlog.get_logger()


class MongoOrderRepository(OrderRepositoryPort):
    """Implementação do repositório usando MongoDB."""

    def __init__(self, database: AsyncIOMotorDatabase, collection_name: str = "orders") -> None:
        """
        Inicializa o repositório MongoDB.

        Args:
            database: Instância do banco de dados MongoDB
            collection_name: Nome da coleção
        """
        self._collection = database[collection_name]
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        """Cria índices necessários."""
        # Índice único no ID do pedido
        # Nota: Em produção, isso deveria ser feito via migration
        pass

    async def save(self, order: Order) -> Order:
        """
        Salva ou atualiza um pedido no MongoDB.

        Args:
            order: Pedido a ser salvo

        Returns:
            Pedido salvo
        """
        order_dict = self._order_to_dict(order)

        try:
            await self._collection.update_one(
                {"id": order.id},
                {"$set": order_dict},
                upsert=True,
            )
            logger.debug("Pedido salvo no MongoDB", order_id=str(order.id))
        except DuplicateKeyError as e:
            logger.error("Erro ao salvar pedido", order_id=str(order.id), error=str(e))
            raise

        return order

    async def find_by_id(self, order_id: OrderId) -> Order | None:
        """
        Busca um pedido por ID no MongoDB.

        Args:
            order_id: ID do pedido

        Returns:
            Pedido encontrado ou None
        """
        document = await self._collection.find_one({"id": order_id})

        if not document:
            return None

        return self._dict_to_order(document)

    def _order_to_dict(self, order: Order) -> dict[str, Any]:
        """
        Converte entidade Order para dicionário MongoDB.

        Args:
            order: Entidade Order

        Returns:
            Dicionário para MongoDB
        """
        return {
            "id": order.id,
            "customer_id": order.customer_id,
            "items": order.items,
            "total_amount": {
                "amount": float(order.total_amount.amount),
                "currency": order.total_amount.currency,
            },
            "status": order.status.value,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
        }

    def _dict_to_order(self, document: dict[str, Any]) -> Order:
        """
        Converte dicionário MongoDB para entidade Order.

        Args:
            document: Documento do MongoDB

        Returns:
            Entidade Order
        """
        # Converte datetime se vier como string
        created_at = document.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

        updated_at = document.get("updated_at")
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))

        total_amount_dict = document.get("total_amount", {})
        money = Money(
            amount=total_amount_dict.get("amount", 0),
            currency=total_amount_dict.get("currency", "BRL"),
        )

        return Order(
            order_id=OrderId(document["id"]),
            customer_id=document["customer_id"],
            items=document.get("items", []),
            total_amount=money,
            status=OrderStatus(document["status"]),
            created_at=created_at,
            updated_at=updated_at,
        )
