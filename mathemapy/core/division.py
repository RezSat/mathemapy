from .operators import BinaryOperator
from .numbers import Number

class Division(BinaryOperator):
    symbol = '/'

    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
            if right_val == 0:
                return "Division by zero!"# Hanldling division by zero
            return Number(left_val / right_val)
        return self #Return the Node itself if not fully evaluatable