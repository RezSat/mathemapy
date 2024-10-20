class Multiplication:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        e_left = self.left.evaluate()
        e_right = self.right.evaluate()

        return e_left * e_right

    def __repr__(self):
        return f"({self.left} * {self.right})"