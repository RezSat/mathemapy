from .expr import Expression
from .numbers import Number
from .symbol import Symbol
from collections import defaultdict

class Add(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(self.left, Number) and isinstance(self.right, Number):
            return Number(eval_left.value + eval_right)
        
        return self.simplify()

    def simplify(self):
        from .mul import Mul
        
        left_simple = self.left.simplify()
        right_simple = self.right.simplify()

        # If both operands are numbers, compute the  result
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            return Number(left_simple.value + right_simple.value)
        
        # Logic to combine like terms...abs
        self.terms = defaultdict(lambda: Number(0))

        # Collect terms form both sides
        self.collect_terms(left_simple)
        self.collect_terms(right_simple)

        # Constrcut the simplified expression
        result = None
        # the reason for sorting is for conistent output
        sorted_terms = sorted(self.terms.items(), key=lambda x : str(x[0]))
        
        for term, coeff in sorted_terms:
            if coeff.value == 0:
                continue

            term_expr = None
            if term == Number(1):
                term_expr = coeff
            elif coeff.value == 1:
                term_expr = term
            else:
                term_expr = Mul(coeff, term)

            if result is None:
                result = term_expr
            else:
                result = Add(result, term_expr)

        return result if result is not None else Number(0)
    
    def alternative(self):
        return self

    def collect_terms(self,expr):
        """
            Recursively collect terms from nested additions
        """
        if isinstance(expr, Add):
            self.collect_terms(expr.left)
            self.collect_terms(expr.right)
        else:
            self.add_term(expr)

    def add_term(self, expr, coefficient=Number(1)):
        from .mul import Mul

        if isinstance(expr, Number):
            self.terms[Number(1)] = Number(self.terms[Number(1)].value + expr.value)
        elif isinstance(expr, Symbol):
            self.terms[expr] = Number(self.terms[expr].value  + coefficient.value )
        elif isinstance(expr, Mul):
            # Handle cases like 2*x + 3*x
            if isinstance(expr.left, Number) and isinstance(expr.right, Symbol):
                self.terms[expr.right] = Number(self.terms[expr.right].value + expr.left.value)
            elif isinstance(expr.right, Number) and isinstance(expr.left, Symbol):
                self.terms[expr.left] = Number(self.terms[expr.left].value + expr.right.value)

            #Handle cases like 2*(x*y) + 3*(x*y)

            elif isinstance(expr.left, Number) and isinstance(expr.right, Mul):
                self.terms[expr.right] = Number(self.terms[expr.right].value + expr.left.value)
            elif isinstance(expr.right, Number) and isinstance(expr.left, Mul):
                self.terms[expr.left] = Number(self.terms[expr.left].value + expr.right.value)

            else:
                self.terms[expr] = Number(self.terms[expr].value + coefficient.value)
        else:
            self.terms[expr] = Number(self.terms[expr].value + coefficient.value)
        

    def __str__(self):
        return f'({self.left} + {self.right})'