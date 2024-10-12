from .operators import UnaryOperator
from .numbers import Number
from .symbol import Symbol
from .multiplication import Multiplication

class Negate(UnaryOperator):
    symbol = '-'

    def __init__(self, operand):
        self.operand = operand
        if isinstance(operand, Number):
            self.operand = Number(-operand.value)
        if isinstance(operand, Symbol):
            self.operand = Multiplication(Number(-1), operand)

    def evaluate(self):
        return self.operand

    def __repr__(self):
        return f"-{self.operand}"