"""Routers FastAPI para endpoints da API."""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from src.adapters.http.dependencies import (
    get_create_order_use_case,
    get_get_order_use_case,
    get_update_order_status_use_case,
)
from src.adapters.http.schemas import (
    CreateOrderRequest,
    OrderResponse,
    UpdateOrderStatusRequest,
)
from src.application.use_cases.create_order import CreateOrderUseCase
from src.application.use_cases.get_order import GetOrderUseCase
from src.application.use_cases.update_order_status import UpdateOrderStatusUseCase
from src.domain.exceptions import (
    InvalidStatusTransitionError,
    OrderNotFoundError,
)
from src.domain.value_objects.order_id import OrderId
from src.domain.value_objects.order_status import OrderStatus

logger = structlog.get_logger()

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequest,
    create_order_use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
) -> OrderResponse:
    """
    Cria um novo pedido.

    Args:
        request: Dados do pedido
        create_order_use_case: Caso de uso de criação

    Returns:
        Pedido criado
    """
    try:
        order = await create_order_use_case.execute(
            customer_id=request.customer_id,
            items=request.items,
            total_amount=request.total_amount,
        )

        return OrderResponse(**order.to_dict())
    except Exception as e:
        logger.error("Erro ao criar pedido", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar pedido",
        ) from e


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    get_order_use_case: GetOrderUseCase = Depends(get_get_order_use_case),
) -> OrderResponse:
    """
    Obtém um pedido por ID.

    Args:
        order_id: ID do pedido
        get_order_use_case: Caso de uso de busca

    Returns:
        Pedido encontrado
    """
    try:
        order = await get_order_use_case.execute(OrderId(order_id))
        return OrderResponse(**order.to_dict())
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Erro ao buscar pedido", order_id=order_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar pedido",
        ) from e


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    request: UpdateOrderStatusRequest,
    update_order_status_use_case: UpdateOrderStatusUseCase = Depends(
        get_update_order_status_use_case
    ),
) -> OrderResponse:
    """
    Atualiza o status de um pedido.

    Args:
        order_id: ID do pedido
        request: Novo status
        update_order_status_use_case: Caso de uso de atualização

    Returns:
        Pedido atualizado
    """
    try:
        new_status = OrderStatus(request.status)
        order = await update_order_status_use_case.execute(
            OrderId(order_id),
            new_status,
        )
        return OrderResponse(**order.to_dict())
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except (InvalidStatusTransitionError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error(
            "Erro ao atualizar status do pedido",
            order_id=order_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar status do pedido",
        ) from e
