from .node import Node
from decimal import Decimal

class Number(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

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

    """     
    def __add__(self, other):
        if isinstance(other, Integer):
            return Addition(self, other)#Integer(self.value + other.value)
        elif isinstance(other, int):
            return Addition(self,Integer(other))#Integer(self.value + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Integer):
            return Subtraction(self,other)#Integer(self.value - other.value)
        elif isinstance(other, int):
            return Subtraction(self, Integer(other))#Integer(self.value - other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Multiplication(self,other)# Integer(self.value * other.value)
        elif isinstance(other, int):
            return Multiplication(self, Integer(other))#Integer(self.value * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Integer):
            return Division(self,other)#Float(self.value / other.value)
        elif isinstance(other, int):
            return Division(self, Integer(other))#Float(self.value / other)
        return NotImplemented
    """
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
    """
    # Allow interaction with Python's float type
    def __add__(self, other):
        if isinstance(other, Float):
            return Addition(self,other)#Float(self.value + other.value)
        elif isinstance(other, (int, float)):
            return Addition(self, Float(other))#Float(self.value + Decimal(str(other)))
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Float):
            return Subtraction(self,other)# Float(self.value - other.value)
        elif isinstance(other, (int, float)):
            return Subtraction(self, Float(other))# Float(self.value - Decimal(str(other)))
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Float):
            return Multiplication(self,other)# Float(self.value * other.value)
        elif isinstance(other, (int, float)):
            return Multiplication(self, Float(other))# Float(self.value * Decimal(str(other)))
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Float):
            return Division(self,other)# Float(self.value / other.value)
        elif isinstance(other, (int, float)):
            return Division(self, Float(other))# Float(self.value / Decimal(str(other)))
        return NotImplemented
    """    
    def __repr__(self):
        return f"{self.evaluate():.{self.preceision}f}"
    


