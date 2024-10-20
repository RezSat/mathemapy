class Symbol:
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        return self.name

    def __add__(self, other):
        from .addition import Addition
        return Addition(self, other)

    def __sub__(self, other):
        from .subtraction import Subtraction
        return Subtraction(self, other)

    def __repr__(self):
        return str(self.name)