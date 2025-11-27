"""Adapter RabbitMQ para publicação de eventos."""

import json
from datetime import datetime

import aio_pika
import structlog
from aio_pika import Connection, Exchange, ExchangeType

from src.domain.ports.message_broker_port import MessageBrokerPort

logger = structlog.get_logger()


class RabbitMQPublisher(MessageBrokerPort):
    """Implementação do publisher usando RabbitMQ."""

    def __init__(
        self,
        connection: Connection,
        exchange_name: str = "order_events",
        routing_key: str = "order.status_updated",
    ) -> None:
        """
        Inicializa o publisher RabbitMQ.

        Args:
            connection: Conexão RabbitMQ
            exchange_name: Nome do exchange
            routing_key: Chave de roteamento padrão
        """
        self._connection = connection
        self._exchange_name = exchange_name
        self._routing_key = routing_key
        self._exchange: Exchange | None = None

    async def connect(self) -> None:
        """Estabelece conexão e cria exchange."""
        channel = await self._connection.channel()
        self._exchange = await channel.declare_exchange(
            self._exchange_name, ExchangeType.TOPIC, durable=True
        )
        logger.info("Conectado ao RabbitMQ", exchange=self._exchange_name)

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
        if not self._exchange:
            await self.connect()

        event = {
            "order_id": order_id,
            "old_status": old_status,
            "new_status": new_status,
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "order.status_updated",
        }

        message_body = json.dumps(event).encode()

        await self._exchange.publish(
            aio_pika.Message(
                message_body,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self._routing_key,
        )

        logger.info(
            "Evento publicado no RabbitMQ",
            order_id=order_id,
            old_status=old_status,
            new_status=new_status,
        )
