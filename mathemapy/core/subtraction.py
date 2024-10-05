from .operators import BinaryOperator
from .numbers import Number
from .symbol import Symbol
from .multiplication import Multiplication
from .node import Node

class Subtraction(BinaryOperator):
    symbol = '-'
    
    def __init__(self, left, right):
        super().__init__(left, right)
        flat_terms = self._flattern(left, self._negate(right))
        self.terms = self._collect_like_terms(flat_terms)

    def evaluate(self):
        evaluated_terms = [ term.evaluate() if isinstance(term, Node) else term for term in self.terms ]
        numeric_diff = Number(sum([term for term in evaluated_terms if isinstance(term, (int, float))]))

        remaining_terms = [ term for term in evaluated_terms if not isinstance(term, (int, float)) ]
        if numeric_diff != 0:
            remaining_terms.insert(0, numeric_diff)
        if len(remaining_terms) == 1:
            return remaining_terms[0]  # If only one term, return it
        return self._group_as_binary_subtraction(remaining_terms)

    def _group_as_binary_subtraction(self, terms):
        """
        Recursively groups terms into nested Subtraction nodes
        Takes a list of terms and returns a Subtraction object that respects binary structure
        """
        if len(terms) == 2:
            return Subtraction(terms[0], terms[1])
        else:
            # Recursively group terms: Subtraction(left, Subtraction(remain terms))
            return Subtraction(terms[0], self._group_as_binary_subtraction(terms[1:]))

    def _flattern(self, *terms):
        operands = []
        for term in terms:
            if isinstance(term, Subtraction):
                operands.extend(term._flattern(term.left, self._negate(term.right)))
            else:
                operands.append(term)
        return operands

    def _collect_like_terms(self, terms):
        collected = {}
        for term in terms:
            if isinstance(term, Number):
                collected['number'] = collected.get('number', 0) + term.value
            elif isinstance(term, Symbol):
                if term.name in collected:
                    collected[term.name] += 1  # Increment coefficient
                else:
                    collected[term.name] = 1
            elif isinstance(term, Multiplication):
                base, coeff = term.left, term.right
                if isinstance(base, Symbol) and isinstance(coeff, Number):
                    if base.name in collected:
                        collected[base.name] += coeff.value
                    else:
                        collected[base.name] = coeff.value
            else:
                collected[term] = collected.get(term, 0) + 1

        # Rebuild terms based on collected results
        result = []
        if 'number' in collected and collected['number'] != 0:
            result.append(Number(collected['number']))
        for term, coeff in collected.items():
            if term != 'number' and coeff != 0:
                if coeff == 1:
                    result.append(term)
                else:
                    result.append(Multiplication(Number(coeff), Symbol(term)))
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
