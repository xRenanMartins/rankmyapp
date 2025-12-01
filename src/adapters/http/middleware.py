"""Middlewares para a aplicação."""

import uuid
from collections.abc import Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware para adicionar correlation ID às requisições."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Adiciona correlation ID à requisição.

        Args:
            request: Requisição HTTP
            call_next: Próximo middleware/handler

        Returns:
            Resposta HTTP
        """
        # Tenta obter correlation ID do header, senão gera um novo
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

        # Adiciona ao state da requisição
        request.state.correlation_id = correlation_id

        # Adiciona ao contexto do logger
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

        # Processa a requisição
        response = await call_next(request)

        # Adiciona correlation ID ao header da resposta
        response.headers["X-Correlation-ID"] = correlation_id

        return response



