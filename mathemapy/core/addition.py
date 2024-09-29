from .operators import BinaryOperator
from .numbers import Number
from .symbol import Symbol
from .multiplication import Multiplication
from .node import Node

class Addition(BinaryOperator):
    symbol = '+'
    def __init__(self, left, right):
        super().__init__(left, right)
        flat_terms = self._flattern(left,right)
        self.terms = self._collect_like_terms(flat_terms)

    def evaluate(self):
        evaluated_terms = [ term.evaluate() if isinstance(term, Node) else term for term in self.terms ]
        numeric_sum = Number(sum([term for term in evaluated_terms if isinstance(term, (int, float))]))

        remaining_terms = [ term for term in evaluated_terms if not isinstance(term, (int, float)) ]
        if numeric_sum != 0:
            remaining_terms.insert(0, numeric_sum)
        if len(remaining_terms) == 1:
            return remaining_terms[0] # If only one term, return it
        return self._group_as_binary_addition(remaining_terms)

    def _group_as_binary_addition(self, terms):
        """
        Recursively groups terms into nested Addition nodes
        Takes a list of terms and returns an Additon object that respects binary structure
        """
        if len(terms) == 2:
            return Addition(terms[0], terms[1])
        else:
            #Recursively group terms: Addition(left, Addition(remain terms))
            return Addition(terms[0], self._group_as_binary_addition(terms[1:]))
        
    def _flattern(self, *terms):
        operands = []
        for term in terms:
            if isinstance(term, Addition):
                operands.extend(term._flattern(term.left, term.right))
            else:
                operands.append(term)
        return operands

    def _collect_like_terms(self, terms):
        collected = {}
        for term in terms:
            if isinstance(term, Number):
                collected['number'] = collected.get('number', 0) + term.value
            elif isinstance(term, Symbol):
                collected[term.name] = collected.get(term.name, 0) + 1
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

    def __repr__(self):
        return " + ".join([repr(term) for term in self.terms])