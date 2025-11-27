"""Aplicação principal FastAPI."""

import logging

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.http.health import router as health_router
from src.adapters.http.routers import router as orders_router
from src.app.container import container

# Configurar logging estruturado
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(
    title="Order Management Service",
    description="Serviço de gerenciamento de pedidos de e-commerce",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router)
app.include_router(orders_router)


@app.on_event("startup")
async def startup_event() -> None:
    """Inicializa dependências na startup."""
    logger.info("Iniciando aplicação")
    await container.initialize()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Finaliza dependências no shutdown."""
    logger.info("Finalizando aplicação")
    await container.shutdown()
