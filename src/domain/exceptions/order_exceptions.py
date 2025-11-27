"""Exceções relacionadas a pedidos."""


class OrderNotFoundError(Exception):
    """Exceção lançada quando um pedido não é encontrado."""

    pass


class InvalidStatusTransitionError(Exception):
    """Exceção lançada quando uma transição de status é inválida."""

    pass
