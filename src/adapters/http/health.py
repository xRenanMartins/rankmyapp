"""Endpoint de healthcheck."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Endpoint de healthcheck simples.

    Returns:
        Status da aplicação
    """
    return {"status": "healthy"}
