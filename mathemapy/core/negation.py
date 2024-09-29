from .operators import UnaryOperator
from .numbers import Number

class Negation(UnaryOperator):
    symbol = '-'

    def evaluate(self):
        operand_val = self.operand.evaluate()

        if isinstance(operand_val, (int, float)):
            return Number(-operand_val)
        return self #Return the Node itself if not fully evaluatable
