from .operators import BinaryOperator
from .numbers import Number
from .symbol import Symbol
from .node import Node
from .multiplication import Multiplication
from .negation import Negate

class Subtraction(BinaryOperator):
    symbol = '-'

    def __init__(self, left, right):
        super().__init__(left, right)
        flat_terms = self._flattern(left, right)
        self.terms = self._collect_like_terms(flat_terms)

    def evaluate(self):
        evaluated_terms = [term.evaluate() if isinstance(term, Node) else term for term in self.terms]
        numeric_difference = evaluated_terms[0] if isinstance(evaluated_terms[0], (int, float, Number)) else Number(evaluated_terms[0])

        #Subtract all numerice terms
        for term in evaluated_terms[1:]:
            if isinstance(term, (int, float)):
                numeric_difference -= term
            elif isinstance(term, Number):
                numeric_difference = Number(numeric_difference-term.value)
        
        remaining_terms = [term for term in evaluated_terms if not isinstance(term, (int, float, Number))]

        if numeric_difference != 0:
            remaining_terms.insert(0, Number(numeric_difference))
        if len(remaining_terms) == 1:
            return remaining_terms[0] # return a single term if only one term remaining

        return self._group_as_binary_subtraction(remaining_terms)

    def _group_as_binary_subtraction(self, terms):
        """
        Recursively groups terms into nested substraction nodes. 
        Takes a list of terms and returns a Subtraction object that 
        respects binary structure
        """
        if len(terms) == 2:
            return Subtraction(terms[0], terms[1])
        else:
            #Recursively groyp terms: Sutraction(lft, Subtration(remain terms..))
            return Subtraction(terms[0], self._group_as_binary_subtraction(terms[1:]))
    
    def _flattern(self, *terms):
        # terms[0] -> left node
        # terms[1] -> right node -> should negate
        # for now we just do this manually

        operands = []
        if isinstance(terms[0], Subtraction):
            operands.extend(terms[0]._flattern(terms[0].left, terms[0].right))
        # this code will be same for term[1] and this handles the cases like
        # Negate(Subtraction())
        # because we know that if a right node is subtraction node it will be auto negate
        # and do a flattern again so there will be a neagtion node next run instead of a subtraction node
        # so that if this code was not here that negation of the subtraction node wil not be handled.abs

        # latter at some point we neeed to generalize all of these but for now doing it manually

        elif isinstance(terms[0], Negate):
            if isinstance(terms[0].operand, Subtraction):
                operands.extend(terms[0].operand._flattern(Negate(terms[0].operand.left), Negate(terms[0].operand.right)))
            else:
                operands.append(terms[0])
        else:
            operands.append(terms[0])

        if isinstance(terms[1], Subtraction):
            # since this is the right node, both left and right node belongs here
            # will subjected to a negation
            operands.extend(terms[1]._flattern(Negate(terms[1].left), Negate(terms[1].right)))
        elif isinstance(terms[1], Negate):
            if isinstance(terms[1].operand, Subtraction):
                operands.extend(terms[1].operand._flattern(Negate(terms[1].operand.left), Negate(terms[1].operand.right)))
            else:
                operands.append(terms[1])
        else:
            operands.append(Negate(terms[1])) # we negate each right term.
        print(operands)
        return operands

    def _collect_like_terms(self,terms):
        collected = {}
        for index,term in enumerate(terms):
            if isinstance(term, Number):
                #collect numbers
                collected['number'] = collected.get('number', terms[0].value) if index == 0 else collected.get('number', 0) - term.value
            elif isinstance(term, Symbol):
                # collect symbols
                if term.name in collected:
                    collected[term.name] -= 1 #Decrese the coefficient
                else:
                    collected[term.name] = 1 if index == 0 else -1
            elif isinstance(term, Multiplication):
                base, coeff = term.left, term.right
                if isinstance(base, Symbol) and isinstance(coeff, Number):
                    if base.name in collected:
                        collected[base.name] -= coeff.value
                    else:
                        collected[base.name] = coeff.value if index == 0 else -coeff.value
            else:
                collected[term] = collected.get(term, 0) -1

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
