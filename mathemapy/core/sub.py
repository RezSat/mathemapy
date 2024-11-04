from .expr import Expression
from .numbers import Number
from .ad import Add

class Sub(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        return Add(self.left, Mul(Number(-1), self.right)).evaluate()
    
    def simplify(self):
        return Add(self.left, Mul(Number(-1), self.right)).simplify()

    def __str__(self):
        return f"({self.left} - {self.right})"
    
