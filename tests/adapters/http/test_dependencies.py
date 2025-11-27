"""Testes para dependency functions."""

from unittest.mock import MagicMock

import pytest

from src.adapters.http.dependencies import (
    get_create_order_use_case,
    get_get_order_use_case,
    get_update_order_status_use_case,
)
from src.app.container import container


@pytest.fixture
def mock_container():
    """Cria mock do container."""
    mock_repo = MagicMock()
    mock_broker = MagicMock()

    # Salvar valores originais
    original_repo = container._repository
    original_broker = container._message_broker

    # Configurar mocks
    container._repository = mock_repo
    container._message_broker = mock_broker

    yield container

    # Restaurar valores originais
    container._repository = original_repo
    container._message_broker = original_broker


def test_get_create_order_use_case(mock_container):
    """Testa get_create_order_use_case."""
    use_case = get_create_order_use_case()

    assert use_case is not None
    assert hasattr(use_case, "execute")


def test_get_get_order_use_case(mock_container):
    """Testa get_get_order_use_case."""
    use_case = get_get_order_use_case()

    assert use_case is not None
    assert hasattr(use_case, "execute")


def test_get_update_order_status_use_case(mock_container):
    """Testa get_update_order_status_use_case."""
    use_case = get_update_order_status_use_case()

    assert use_case is not None
    assert hasattr(use_case, "execute")
