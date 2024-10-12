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

    def _compare_same_type(self, other):
        if self.symbol == other.symbol == "+":
            return self.terms == other.terms
        elif self.symbol == other.symbol == '-':
            return self.terms == other.terms
        elif self.symbol == other.symbol == '*':
            return self.factors == other.factors
        elif self.symbol == other.symbol == "^":
            print('came here')
            return self.base == other.base and self.exponent == other.exponent
        return self.left == other.left and self.right == other.right

    def _get_hash_value(self):
        return (self.left, self.right)

    def __repr__(self):

        """
        Return a string representation of the binary operator.
        
        The representation is in the form "(left operator right)".
        """
        
        return f"({repr(self.left)} {self.symbol} {repr(self.right)})"

class UnaryOperator(Operator):
    def __init__(self, operand):
        self().__init__()
        self.operand = operand

    def _get_hash_value(self):
        return self.operand

    def _compare_same_type(self, other):
        return isinstance(other, UnaryOperator) and self.operand == other.operand

    def __repr__(self):
        return f"({self.symbol}{repr(self.operand)})"

