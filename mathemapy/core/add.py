from .expr import Expression
from .numbers import Number

class Add(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return Number(eval_left.value + eval_right)
        
        return self.simplify()

    def simplify(self):
        left_simple = self.left.simplify()
        right_simple = self.right.simplify()

        # If both operands are numbers, compute the  result
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            return Number(left_simple.value + right_simple.value)
        
        # Logic to combine like terms...abs
        

    def __str__(self):
        return f'({self.left} + {self.right})'