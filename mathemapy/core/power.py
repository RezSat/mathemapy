from .operators import BinaryOperator
from .numbers import Number
from .symbol import Symbol
from .node import Node

class Power(BinaryOperator):
    symbol = '^'

    def __init__(self, base, exponent):
        super().__init__(base, exponent)
        self.base, self.exponent = self._flattern(base, exponent)

    def evaluate(self):
        evaluated_base = self.base.evaluate() if isinstance(self.base, Node) else self.base
        evaluated_exponent = self.exponent.evaluate() if isinstance(self.exponent, Node) else self.exponent

        # Handle the case of 0^0 which is generally considered undefined or 1 in some cases
        if isinstance(evaluated_base, (int, float)) and evaluated_base == 0 and isinstance(evaluated_exponent, (int, float)) and evaluated_exponent == 0:
            raise ValueError("0^0 is undefined.")

        # Handle numerical exponentiation
        if isinstance(evaluated_base, (int, float)) and isinstance(evaluated_exponent, (int, float)):
            return Number(evaluated_base ** evaluated_exponent)

        if evaluated_exponent == 1:
            return evaluated_base  # x^1 = x
        if evaluated_base == 1:
            return Number(1)  # 1^x = 1
        if evaluated_exponent == 0:
            return Number(1)  # x^0 = 1 for any x != 0
        return Power(Symbol(evaluated_base), evaluated_exponent)

    def _flattern(self, base, exponent):
        """
        Flatten nested power expressions.
        """
        if isinstance(base, Power):
            base, _ = base._flattern(base.base, base.exponent)
        if isinstance(exponent, Power):
            _, exponent = exponent._flattern(exponent.base, exponent.exponent)
        return base, exponent