"""Testes para endpoint de healthcheck."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.adapters.http.health import router

app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    """Cria cliente de teste."""
    return TestClient(app)


def test_health_check(client):
    """Testa endpoint de healthcheck."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
