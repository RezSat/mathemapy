from .node import Node
from decimal import Decimal

class Number(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value
    
    def _get_hash_value(self):
        return self.value

    def _compare_same_type(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, float):
            return self.value == other
        if isinstance(other, Number):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash((self.__class__, self._get_hash_value()))

    def __repr__(self):
        return str(self.value)    

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
    


