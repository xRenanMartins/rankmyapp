"""Container de dependency injection."""

import structlog
from aio_pika import Connection, connect_robust
from motor.motor_asyncio import AsyncIOMotorClient

from src.adapters.messaging.rabbitmq_publisher import RabbitMQPublisher
from src.adapters.persistence.mongo_order_repository import MongoOrderRepository
from src.app.config import settings
from src.application.use_cases.create_order import CreateOrderUseCase
from src.application.use_cases.get_order import GetOrderUseCase
from src.application.use_cases.update_order_status import UpdateOrderStatusUseCase

logger = structlog.get_logger()


class Container:
    """Container para dependency injection."""

    def __init__(self) -> None:
        """Inicializa o container."""
        self._mongo_client: AsyncIOMotorClient | None = None
        self._rabbitmq_connection: Connection | None = None
        self._repository: MongoOrderRepository | None = None
        self._message_broker: RabbitMQPublisher | None = None

    async def initialize(self) -> None:
        """Inicializa conexões e dependências."""
        try:
            # MongoDB
            logger.info("Conectando ao MongoDB", url=settings.mongodb_url)
            self._mongo_client = AsyncIOMotorClient(settings.mongodb_url)
            database = self._mongo_client[settings.mongodb_db_name]
            self._repository = MongoOrderRepository(database)

            # Garantir que os índices sejam criados
            await self._repository._ensure_indexes()
            logger.info("MongoDB conectado e índices verificados")
        except Exception as e:
            logger.error("Erro ao conectar ao MongoDB", error=str(e), error_type=type(e).__name__)
            raise

        try:
            # RabbitMQ
            logger.info("Conectando ao RabbitMQ", url=settings.rabbitmq_url)
            self._rabbitmq_connection = await connect_robust(settings.rabbitmq_url)
            self._message_broker = RabbitMQPublisher(
                self._rabbitmq_connection,
                exchange_name=settings.rabbitmq_exchange,
                routing_key=settings.rabbitmq_routing_key,
            )
            await self._message_broker.connect()
            logger.info("RabbitMQ conectado")
        except Exception as e:
            logger.error("Erro ao conectar ao RabbitMQ", error=str(e), error_type=type(e).__name__)
            # Fecha MongoDB se RabbitMQ falhar
            if self._mongo_client:
                self._mongo_client.close()
            raise

        logger.info("Container inicializado com sucesso")

    async def shutdown(self) -> None:
        """Fecha conexões."""
        try:
            if self._mongo_client:
                self._mongo_client.close()
                logger.info("Conexão MongoDB fechada")
        except Exception as e:
            logger.error("Erro ao fechar conexão MongoDB", error=str(e))

        try:
            if self._rabbitmq_connection:
                await self._rabbitmq_connection.close()
                logger.info("Conexão RabbitMQ fechada")
        except Exception as e:
            logger.error("Erro ao fechar conexão RabbitMQ", error=str(e))

        logger.info("Container finalizado")

    def get_create_order_use_case(self) -> CreateOrderUseCase:
        """Retorna instância do caso de uso de criação."""
        if not self._repository:
            raise RuntimeError("Container não inicializado")
        return CreateOrderUseCase(self._repository)

    def get_get_order_use_case(self) -> GetOrderUseCase:
        """Retorna instância do caso de uso de busca."""
        if not self._repository:
            raise RuntimeError("Container não inicializado")
        return GetOrderUseCase(self._repository)

    def get_update_order_status_use_case(self) -> UpdateOrderStatusUseCase:
        """Retorna instância do caso de uso de atualização."""
        if not self._repository or not self._message_broker:
            raise RuntimeError("Container não inicializado")
        return UpdateOrderStatusUseCase(self._repository, self._message_broker)


container = Container()
