from .expr import Expression

class Symbol(Expression):
    def __init__(self, name:  str):
        self.name = name

    def evaluate(self):
        return self.name # unsure what to here

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

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)
    
