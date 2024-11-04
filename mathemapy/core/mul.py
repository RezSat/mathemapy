from .expr import Expression
from .numbers import Number

class Mul(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left * eval_right)

        return self.simplify()
    
    def simplify(self):
        left_simple = self.left.simplify()
        right_simple = self.right.simplify()
        
        # Collect terms for multiplication
        terms = defaultdict(lambda: Number(0))  # For exponents
        coefficient = Number(1)
        
        def collect_factors(expr, power=Number(1)):
            nonlocal coefficient
            if isinstance(expr, Number):
                coefficient = Number(coefficient.value * expr.value)
            elif isinstance(expr, Mul):
                collect_factors(expr.left)
                collect_factors(expr.right)
            elif isinstance(expr, Pow):
                base = expr.left
                if isinstance(expr.right, Number):
                    collect_factors(base, expr.right)
                else:
                    terms[expr] = Number(terms[expr].value + power.value)
            else:
                terms[expr] = Number(terms[expr].value + power.value)
        
        collect_factors(left_simple)
        collect_factors(right_simple)
        
        # If coefficient is 0, return 0
        if coefficient.value == 0:
            return Number(0)
        
        # Construct the result
        result = None
        sorted_terms = sorted(terms.items(), key=lambda x: str(x[0]))
        
        for base, exponent in sorted_terms:
            if exponent.value == 0:
                continue
                
            term = base if exponent.value == 1 else Pow(base, exponent)
            
            if result is None:
                result = term
            else:
                result = Mul(result, term)
        
        if result is None:
            return coefficient
        
        return result if coefficient.value == 1 else Mul(coefficient, result)

    def __str__(self):
        return f"({self.left} * {self.right})"
                
