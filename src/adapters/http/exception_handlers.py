"""Exception handlers globais para a aplicação."""


import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import InvalidStatusTransitionError, OrderNotFoundError

logger = structlog.get_logger()


async def order_not_found_handler(request: Request, exc: OrderNotFoundError) -> JSONResponse:
    """
    Handler para exceção de pedido não encontrado.

    Args:
        request: Requisição HTTP
        exc: Exceção lançada

    Returns:
        Resposta JSON com erro 404
    """
    correlation_id = getattr(request.state, "correlation_id", None)
    logger.warning(
        "Pedido não encontrado",
        path=request.url.path,
        correlation_id=correlation_id,
        error=str(exc),
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc), "error_type": "OrderNotFoundError"},
    )


async def invalid_status_transition_handler(
    request: Request, exc: InvalidStatusTransitionError
) -> JSONResponse:
    """
    Handler para exceção de transição de status inválida.

    Args:
        request: Requisição HTTP
        exc: Exceção lançada

    Returns:
        Resposta JSON com erro 400
    """
    correlation_id = getattr(request.state, "correlation_id", None)
    logger.warning(
        "Transição de status inválida",
        path=request.url.path,
        correlation_id=correlation_id,
        error=str(exc),
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "error_type": "InvalidStatusTransitionError"},
    )


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """
    Handler para exceção de valor inválido.

    Args:
        request: Requisição HTTP
        exc: Exceção lançada

    Returns:
        Resposta JSON com erro 400
    """
    correlation_id = getattr(request.state, "correlation_id", None)
    logger.warning(
        "Valor inválido",
        path=request.url.path,
        correlation_id=correlation_id,
        error=str(exc),
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "error_type": "ValueError"},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler genérico para exceções não tratadas.

    Args:
        request: Requisição HTTP
        exc: Exceção lançada

    Returns:
        Resposta JSON com erro 500
    """
    correlation_id = getattr(request.state, "correlation_id", None)
    logger.error(
        "Erro interno do servidor",
        path=request.url.path,
        method=request.method,
        correlation_id=correlation_id,
        error=str(exc),
        error_type=type(exc).__name__,
        exc_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Erro interno do servidor",
            "error_type": type(exc).__name__,
            "correlation_id": correlation_id,
        },
    )


def register_exception_handlers(app) -> None:
    """
    Registra todos os exception handlers na aplicação FastAPI.

    Args:
        app: Instância da aplicação FastAPI
    """
    app.add_exception_handler(OrderNotFoundError, order_not_found_handler)
    app.add_exception_handler(InvalidStatusTransitionError, invalid_status_transition_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
