from .operators import BinaryOperator
from .numbers import Number
from .symbol import Symbol
from .node import Node
from .power import Power

class Multiplication(BinaryOperator):
    symbol = '*'

    def __init__(self, left, right):
        super().__init__(left, right)
        flat_factors = self._flattern(left, right)
        self.factors = self._collect_like_factors(flat_factors)

    def _compare_same_type(self, other):
        return isinstance(other, Multiplication) and self.factors == other.factors

    def evaluate(self):
        evaluated_factors = [ factor.evaluate() if isinstance(factor, Node) else factor for factor in self.factors ]
        numeric_product = Number(self._product([factor for factor in evaluated_factors if isinstance(factor, (int, float))]))

        remaining_factors = [ factor for factor in evaluated_factors if not isinstance(factor, (int, float)) ]
        if numeric_product != 1:  # Don't include 1 in multiplication terms
            remaining_factors.insert(0, numeric_product)
        if len(remaining_factors) == 1:
            return remaining_factors[0]  # If only one factor, return it

        return self._group_as_binary_multiplication(remaining_factors)

    def _group_as_binary_multiplication(self, factors):
        """
        Recursively groups factors into nested Multiplication nodes
        Takes a list of factors and returns a Multiplication object that respects binary structure
        """
        if len(factors) == 2:
            if factors[0] == Number(1) and isinstance(factors[1], Power): # handle the case of 1*(x^n) -> (x^n)
                return factors[1]
            return Multiplication(factors[0], factors[1])
        else:
            # Recursively group factors: Multiplication(left, Multiplication(remain factors))
            return Multiplication(factors[0], self._group_as_binary_multiplication(factors[1:]))

    def _flattern(self, *factors):
        operands = []
        for factor in factors:
            if isinstance(factor, Multiplication):
                operands.extend(factor._flattern(factor.left, factor.right))
            else:
                operands.append(factor)
        
        return operands

    def _collect_like_factors(self, factors):
        collected = {}
        
        for factor in factors:
            if isinstance(factor, Number):
                collected['number'] = collected.get('number', 1) * factor.value  # Multiply numbers
            elif isinstance(factor, Symbol):
                if factor.name in collected:
                    collected[factor.name] += 1  # Increment exponent
                else:
                    collected[factor.name] = 1
            else:
                collected[factor] = collected.get(factor, 1) * 1

        # Rebuild factors based on collected results
        result = []
        if 'number' in collected and collected['number'] != 1:  # Don't include 1 in the results
            result.append(Number(collected['number']))
        for factor, exponent in collected.items():
            if factor != 'number' and exponent != 0:
                if exponent == 1:
                    result.append(Symbol(factor))
                else:
                    result.append(Power(Symbol(factor), Number(exponent)))  # x^n can be written as x * x * x ...\
        return result

    def _product(self, factors):
        """Multiplies a list of numeric factors together."""
        product = 1
        for factor in factors:
            product *= factor
        return product
