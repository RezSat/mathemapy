from .operators import UnaryOperator
from .numbers import Number
from .symbol import Symbol
from .multiplication import Multiplication

class Negate(UnaryOperator):
    symbol = '-'

    def __init__(self, operand):
        from .addition import Addition
        self.operand = operand
        if isinstance(operand, Number):
            self.operand = Number(-operand.value)
        if isinstance(operand, (Symbol, Multiplication, Addition)):
            self.operand = Multiplication(Number(-1), operand)

    def evaluate(self):
        return self.operand