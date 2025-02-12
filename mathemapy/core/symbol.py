from .expr import Expression

class Symbol(Expression):
    def __init__(self, name:  str):
        self.name = name

    def evaluate(self):
        return self.name # unsure what to here

    def simplify(self):
        return self

    def alternative(self):
        return self

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)
    
