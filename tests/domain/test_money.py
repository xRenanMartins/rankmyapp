"""Testes para Money value object."""

from decimal import Decimal

import pytest

from src.domain.value_objects.money import Money


def test_create_money():
    """Testa criação de Money."""
    money = Money(100.0)

    assert money.amount == Decimal("100.0")
    assert money.currency == "BRL"


def test_money_negative_value():
    """Testa que não é possível criar Money com valor negativo."""
    with pytest.raises(ValueError, match="não pode ser negativo"):
        Money(-10.0)


def test_money_equality():
    """Testa igualdade de Money."""
    money1 = Money(100.0)
    money2 = Money(100.0)
    money3 = Money(200.0)

    assert money1 == money2
    assert money1 != money3


def test_money_addition():
    """Testa soma de Money."""
    money1 = Money(50.0)
    money2 = Money(50.0)

    result = money1 + money2

    assert result.amount == Decimal("100.0")


def test_money_addition_different_currency():
    """Testa que não é possível somar Money de moedas diferentes."""
    money1 = Money(50.0, "BRL")
    money2 = Money(50.0, "USD")

    with pytest.raises(ValueError, match="moedas diferentes"):
        money1 + money2


def test_money_multiplication():
    """Testa multiplicação de Money."""
    money = Money(50.0)

    result = money * 2

    assert result.amount == Decimal("100.0")


def test_money_multiplication_float():
    """Testa multiplicação de Money com float."""
    money = Money(50.0)

    result = money * 2.5

    assert result.amount == Decimal("125.0")


def test_money_equality_with_non_money():
    """Testa igualdade de Money com objeto que não é Money."""
    money = Money(100.0)

    assert money != "not money"
    assert money != 100.0
    assert money is not None


def test_money_repr():
    """Testa representação string de Money."""
    money = Money(100.0, "BRL")

    repr_str = repr(money)
    assert "Money" in repr_str
    assert "100.0" in repr_str
    assert "BRL" in repr_str


def test_money_with_decimal():
    """Testa criação de Money com Decimal."""
    from decimal import Decimal

    money = Money(Decimal("100.50"))

    assert money.amount == Decimal("100.50")
    assert money.currency == "BRL"


def test_money_with_int():
    """Testa criação de Money com int."""
    money = Money(100)

    assert money.amount == Decimal("100")
    assert money.currency == "BRL"
