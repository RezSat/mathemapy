class Addition:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        from .number import Number
        from .symbol import Symbol
        from .multiplication import Multiplication

        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return Number(self.left.value + self.right.value)

        if isinstance(self.left, Symbol) and isinstance(self.right, Symbol):
            if  self.left.name == self.right.name:
                return Multiplication(Number(2), Symbol(self.left.name))
        
        e_left = self.left.evaluate()
        e_right = self.right.evaluate()

        return Number(e_left + e_right)

    def __repr__(self):
        return f"({self.left} + {self.right})"