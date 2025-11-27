"""Dependency functions para FastAPI."""

from src.app.container import container


def get_create_order_use_case():
    """Dependency para criar pedido."""
    return container.get_create_order_use_case()


def get_get_order_use_case():
    """Dependency para buscar pedido."""
    return container.get_get_order_use_case()


def get_update_order_status_use_case():
    """Dependency para atualizar status."""
    return container.get_update_order_status_use_case()
