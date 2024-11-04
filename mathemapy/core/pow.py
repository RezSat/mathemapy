from .expr import Expression
from .numbers import Number

class Pow(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left ** eval_right)

        return self.simplify()
    
    def simplify(self):
        left_simple = self.left.simplify()
        right_simple = self.right.simplify()
        
        # Handle numeric powers
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            return Number(left_simple.value ** right_simple.value)
        
        # x^0 = 1
        if isinstance(right_simple, Number) and right_simple.value == 0:
            return Number(1)
        
        # x^1 = x
        if isinstance(right_simple, Number) and right_simple.value == 1:
            return left_simple
        
        # Handle nested powers: (x^a)^b = x^(a*b)
        if isinstance(left_simple, Pow):
            new_exp = Mul(left_simple.right, right_simple).simplify()
            return Pow(left_simple.left, new_exp).simplify()
        
        # 1^x = 1
        if isinstance(left_simple, Number) and left_simple.value == 1:
            return Number(1)
        
        return Pow(left_simple, right_simple)

    def __str__(self):
        return f"({self.left} ^ {self.right})"
        
