from .operators import BinaryOperator
from .numbers import Number
from .symbol import Symbol
from .multiplication import Multiplication
from .node import Node

class DivisionByZeroError(Exception):
    """Custom exception for division by zero."""
    def __init__(self):
        super().__init__("Division by zero is undefined.")

class Division(BinaryOperator):
    symbol = '/'

    def __init__(self, left, right):
        super().__init__(left, right)
        self.numerator, self.denominator = self._flattern(left, right)

    def _compare_same_type(self, other):
        return isinstance(other, Division) and self.numerator == other.numerator and self.denominator == other.denominator

    def evaluate(self):
        evaluated_numerator = self.numerator.evaluate() if isinstance(self.numerator, Node) else self.numerator
        evaluated_denominator = self.denominator.evaluate() if isinstance(self.denominator, Node) else self.denominator

        # Handle division by zero
        if isinstance(evaluated_denominator, (int, float)) and evaluated_denominator == 0:
            raise DivisionByZeroError()

        if isinstance(evaluated_numerator, (int, float)) and isinstance(evaluated_denominator, (int, float)):
            return Number(evaluated_numerator / evaluated_denominator)

        if evaluated_denominator == 1:
            return evaluated_numerator  # x / 1 = x
        return Division(evaluated_numerator, evaluated_denominator)

    def _flattern(self, numerator, denominator):
        """
        Flatten any nested division expressions.
        """
        if isinstance(numerator, Division):
            numerator, _ = numerator._flattern(numerator.numerator, numerator.denominator)
        if isinstance(denominator, Division):
            _, denominator = denominator._flattern(denominator.numerator, denominator.denominator)
        return numerator, denominator