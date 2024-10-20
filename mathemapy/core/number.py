class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __add__(self, other):
        from  .addition import Addition
        return Addition(self, other)
    
    def __sub__(self, other):
        from .subtraction import Subtraction
        return Subtraction(self, other)

    def __repr__(self):
        return str(self.value)
class Integer(Number):
    pass

class Float(Number):
    pass