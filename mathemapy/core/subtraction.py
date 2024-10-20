from .operators import BinaryOperator
from .numbers import Number
from .symbol import Symbol
from .multiplication import Multiplication
from .power import Power
from .node import Node
from .negation import Negate

class Subtraction(BinaryOperator):
    symbol = '+'

    def __init__(self, left, right):
        super().__init__(left, right)
        flat_terms = self._flattern(left,Negate(right).evaluate())
        self.terms = self._collect_like_terms(flat_terms)

    def _compare_same_type(self, other):
        return isinstance(other, Subtraction) and self.terms == other.terms

    def evaluate(self):
        evaluated_terms = [ term.evaluate() if isinstance(term, Node) else term for term in self.terms ]
        numeric_sum = Number(sum([term for term in evaluated_terms if isinstance(term, (int, float))]))
        
        remaining_terms = [ term for term in evaluated_terms if not isinstance(term, (int, float)) ]
        if numeric_sum != 0:
            remaining_terms.insert(0, numeric_sum)
        if len(remaining_terms) == 1:
            return remaining_terms[0] # If only one term, return it
        return self._group_as_binary_subtraction(remaining_terms)

    def _group_as_binary_subtraction(self, terms):
        """
        Recursively groups terms into nested Addition nodes
        Takes a list of terms and returns an Additon object that respects binary structure
        """
        if len(terms) == 2:
            return Subtraction(terms[0], terms[1])
        else:
            #Recursively group terms: Addition(left, Addition(remain terms))
            return Subtraction(terms[0], self._group_as_binary_subtraction(terms[1:]))
        
    def _flattern(self, *terms):
        operands = []
        for term in terms:
            if isinstance(term, Subtraction):
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
                if term.name in collected:
                    collected[term.name] -= 1 # Increment coefficient
                else:
                    collected[term.name] = 1 #collected.get(term.name, 0) + 1
            elif isinstance(term, Multiplication):
                base, coeff = term.right, term.left
                if isinstance(base, Symbol) and isinstance(coeff, Number):
                    if base.name in collected:
                        collected[base.name] -= coeff.value
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
                    result.append(Symbol(term))
                else:
                    result.append(Multiplication(Number(coeff), Symbol(term)))

        return result

    def __repr__(self):
        return "("+"".join([repr(term) for term in self.terms]) + ")"