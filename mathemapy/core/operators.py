from .node import Node

class Operator(Node):
    def __init__(self, *args):
        super().__init__() # If needed for future extensions

    def evaluate(self):
        return NotImplementedError("This method should be implemented by subclasses")

    def __repr__(self):
        return NotImplementedError("This method should be implemented by subclasses")

class BinaryOperator(Operator):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({repr(self.left)} {self.symbol} {repr(self.right)})"

class UnaryOperator(Operator):
    def __init__(self, operand):
        self().__init__()
        self.operand = operand

    def __repr__(self):
        return f"({self.symbol}{repr(self.operand)})"

