from .node import Node
from .expr import Expr
from decimal import Decimal

class Number(Node, Expr):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        return False

class Integer(Number):
    def __init__(self, value):
        if isinstance(value, float):
            raise TypeError("use `Float` class for floating-point numbers")
        elif isinstance(value, int):
            self.value = value
        elif isinstance(value, str):
            self.value = int(value)
        super().__init__(value)

    def evaluate(self):
        return self.value

class Float(Number):
    def __init__(self, value, preceision=15):
        if isinstance(value, float) or isinstance(value, int):
            self.value = Decimal(str(value))
        elif isinstance(value, str):
            self.value = Decimal(value)
        self.preceision = preceision
        super().__init__(value) # Ensure the value is stored as a flaot

    def evaluate(self):
        return round(float(self.value), self.preceision)
   
    def __repr__(self):
        return f"{self.evaluate():.{self.preceision}f}"
    


