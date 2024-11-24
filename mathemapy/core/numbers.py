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

    def __eq__(self, other):
        return isinstance(other, Number) and self.value == other.value
        
    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)        
