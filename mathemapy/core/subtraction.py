from .operators import BinaryOperator
from .numbers import Number
from .symbol import Symbol
from .node import Node
from .multiplication import Multiplication

class Subtraction(BinaryOperator):
    symbol = '-'

    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

    def evaluate(self):
        # Evaluate left and right
        evaluated_left = self.left.evaluate() if isinstance(self.left, Node) else self.left
        evaluated_right = self.right.evaluate() if isinstance(self.right, Node) else self.right

        # If both sides are numeric, return the numeric result
        if isinstance(evaluated_left, Number) and isinstance(evaluated_right, Number):
            return Number(evaluated_left.value - evaluated_right.value)

        # If only the right is numeric and equals zero, return the left side
        if isinstance(evaluated_right, Number) and evaluated_right.value == 0:
            return evaluated_left

        # Return a simplified Subtraction if no further simplification is possible
        return Subtraction(evaluated_left, evaluated_right)

    def _compare_same_type(self, other):
        """
        Compare two Subtraction objects by checking if their left and right sides are equal.
        """
        if isinstance(other, Subtraction):
            return (self.left == other.left) and (self.right == other.right)
        return False

    def __repr__(self):
        return f"({repr(self.left)} - {repr(self.right)})"

    def _negate(self, term):
        """
        Negate the term for handling subtraction, returns a -term expression.
        """
        if isinstance(term, Number):
            return Number(-term.value)
        elif isinstance(term, Multiplication) and isinstance(term.left, Number):
            # If we have something like -1 * x, just negate the number
            return Multiplication(Number(-term.left.value), term.right)
        else:
            # For all other terms, return -1 * term
            return Multiplication(Number(-1), term)

    def flatten(self):
        """
        Flattens nested subtractions: (a - (b - c)) -> (a - b + c).
        This returns a list of terms.
        """
        terms = [self.left]

        if isinstance(self.right, Subtraction):
            terms.append(self.right.left)
            negated_term = self._negate(self.right.right)
            terms.append(negated_term)
        else:
            negated_right = self._negate(self.right)
            terms.append(negated_right)

        return terms

    def collect_like_terms(self):
        """
        Collect like terms: a - a = 0, combine numeric terms, etc.
        """
        terms = self.flatten()

        numeric_sum = 0
        symbol_terms = {}

        for term in terms:
            if isinstance(term, Number):
                numeric_sum += term.value
            elif isinstance(term, Symbol):
                if term.name in symbol_terms:
                    symbol_terms[term.name] += 1
                else:
                    symbol_terms[term.name] = 1
            else:
                # Handle other cases like Multiplications
                if term in symbol_terms:
                    symbol_terms[term] += 1
                else:
                    symbol_terms[term] = 1

        # Build the final result
        result_terms = []
        if numeric_sum != 0:
            result_terms.append(Number(numeric_sum))

        for symbol, coeff in symbol_terms.items():
            if coeff == 1:
                result_terms.append(symbol)
            elif coeff > 1:
                result_terms.append(Multiplication(Number(coeff), symbol))

        # If there's only one term left, return it
        if len(result_terms) == 1:
            return result_terms[0]
        
        # Otherwise, return a nested Subtraction expression
        result = result_terms[0]
        for term in result_terms[1:]:
            result = Subtraction(result, term)

        return result

    def _negate(self, term):
        """Negates a term (used for subtraction)."""
        if isinstance(term, Number):
            return Number(-term.value)
        elif isinstance(term, Multiplication) and isinstance(term.left, Number):
            return Multiplication(Number(-term.left.value), term.right)
        return Multiplication(Number(-1), term)

    def __repr__(self):
        return " - ".join([repr(term) for term in self.terms])
