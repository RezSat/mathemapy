# here we go building the entire core in a single python file
from abc import ABC, abstractmethod
from typing import Union, List

class Expression(ABC):
    """
    expression class is the parent for all other classes
    """

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def simplify(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()
    
# Operators

class Add(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left + eval_right)

        return Add(eval_left, eval_right)
    
    def simplify(self):
        pass

    def __str__(self):
        return f"({self.left} + {self.right})"

class Sub(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left - eval_right)

        return Add(eval_left, eval_right)
    
    def simplify(self):
        pass

    def __str__(self):
        return f"({self.left} - {self.right})"
    
class Mul(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left * eval_right)

        return Add(eval_left, eval_right)
    
    def simplify(self):
        pass

    def __str__(self):
        return f"({self.left} * {self.right})"
    
class Div(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left / eval_right)

        return Add(eval_left, eval_right)
    
    def simplify(self):
        pass

    def __str__(self):
        return f"({self.left} / {self.right})"
    
class Pow(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left ** eval_right)

        return Add(eval_left, eval_right)
    
    def simplify(self):
        pass

    def __str__(self):
        return f"({self.left} ^ {self.right})"
        
class Number(Expression):
    """
    Number class will be the parent for both classes Integer and Float,
    takes an argument of int, or float kind and return the number kind when simplified,
    return an int or float kind when evaluated but needs to be able to work like sympy's 
    number class
    """

    def __init__(self, value: Union[int, float]):
        self.value = value

    def evaluate(self):
        return self.value
    
    def simplify(self):
        return self
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __str__(self):
        return f"{self.value}"
    

class Symbol(Expression):
    """
    Symbol class will represent variable or unknowns kinds in math, 
    they support all basic operations and other algebriac simplifications
    """

    def __init__(self, name: str):
        self.name = name

    def evaluate(self):
        return self

    def simplify(self):
        return self
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)
    
    def __str__(self):
        return f"{self.name}"
    




t = Number(2) + Number(3)
print(t)
print(t.evaluate())
