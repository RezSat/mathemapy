from .expr import Expression
from typing import Union

class Number(Expression):

    """
    Number class will be the parent for Integer and Float classes.
    """
    def __init__(self, value: Union[int, float]):
        self.value = value

    def evaluate(self):
        return self.value

    def simplify(self):
        return self

    """

    def __add__(self, other):
        from .add import Add
        return Add(self, other)

    def __sub__(self, other):
        from .sub import Sub
        return Sub(self, other)

    def __mul__(self, other):
        from .mul import Mul
        return Mul(self, other)

    def __truediv__(self, other):
        from .div import Div
        return Div(self, other)

    def __pow__(self, other):
        from .pow import Pow
        return Pow(self, other)

    """

    def __eq__(self, other):
        return isinstance(other, Number) and self.value == other.value
        
    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)        
