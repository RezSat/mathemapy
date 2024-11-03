from .expr import Expression
from .numbers import Number

class Mul(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return Number(eval_left.value * eval_right.value)
        else:
            return Add(self.left, self.right)

    def simplify(self):
        pass # do something later

    def __str__(self):
        return f'({self.left} * {self.right})'