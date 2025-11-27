"""Value object para valores monetários."""

from decimal import Decimal


class Money:
    """Representa um valor monetário."""

    def __init__(self, amount: Decimal | float | int, currency: str = "BRL") -> None:
        """
        Inicializa um valor monetário.

        Args:
            amount: Valor numérico
            currency: Moeda (padrão: BRL)
        """
        if amount < 0:
            raise ValueError("Valor monetário não pode ser negativo")
        self._amount = Decimal(str(amount))
        self._currency = currency

    @property
    def amount(self) -> Decimal:
        """Retorna o valor numérico."""
        return self._amount

    @property
    def currency(self) -> str:
        """Retorna a moeda."""
        return self._currency

    def __eq__(self, other: object) -> bool:
        """Compara dois valores monetários."""
        if not isinstance(other, Money):
            return False
        return self._amount == other._amount and self._currency == other._currency

    def __repr__(self) -> str:
        """Representação string do objeto."""
        return f"Money(amount={self._amount}, currency={self._currency})"

    def __add__(self, other: "Money") -> "Money":
        """Soma dois valores monetários."""
        if self._currency != other._currency:
            raise ValueError("Não é possível somar valores de moedas diferentes")
        return Money(self._amount + other._amount, self._currency)

    def __mul__(self, factor: int | float) -> "Money":
        """Multiplica o valor por um fator."""
        return Money(self._amount * Decimal(str(factor)), self._currency)
