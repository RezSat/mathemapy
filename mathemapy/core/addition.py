class Addition:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        from .number import Number
        from .symbol import Symbol
        
        e_left = self.left.evaluate()
        e_right = self.right.evaluate()

        return Number(e_left + e_right)

    def __repr__(self):
        return f"({self.left} + {self.right})"