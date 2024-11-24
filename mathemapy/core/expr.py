from abc import ABC, abstractmethod

class Expression(ABC):
    """
    Expression class is the parent for all other classes
    """
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def simplify(self):
        pass

    @abstractmethod
    def alternative(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()
    
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

    def __eq__(self, other: 'Expression') -> bool:
        if not isinstance(other, Expression):
            return False
        # Compare simplified forms
        return str(self.simplify()) == str(other.simplify())

    def __hash__(self):
        return hash(str(self.simplify()))
