from .expr import Expression
from .numbers import Number
from collections import  defaultdict
from .mul import Mul
from .pow import Pow

class Div(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            if eval_right == 0:
                raise ZeroDivisionError("Division by zero")
            return Number(eval_left / eval_right)

        return self.simplify()
    
    def simplify(self):
        left_simple = self.left.simplify()
        right_simple = self.right.simplify()
        
        # Handle division by zero
        if isinstance(right_simple, Number) and right_simple.value == 0:
            raise ZeroDivisionError("Division by zero")
        
        # Handle numeric division
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            if right_simple.value == 0:
                raise ZeroDivisionError("Division by zero")
            return Number(left_simple.value / right_simple.value)
        
        # x/1 = x
        if isinstance(right_simple, Number) and right_simple.value == 1:
            return left_simple
        
        # 0/x = 0 (if x ≠ 0)
        if isinstance(left_simple, Number) and left_simple.value == 0:
            return Number(0)
        
        # x/x = 1 (if x ≠ 0)
        if str(left_simple) == str(right_simple):
            return Number(1)

        # Convert expressions to a canonical form of products
        def get_factors(expr):
            factors = defaultdict(lambda: Number(0))
            coefficient = Number(1)
            
            def collect(e, power=Number(1)):
                nonlocal coefficient
                if isinstance(e, Number):
                    coefficient = Number(coefficient.value * e.value)
                elif isinstance(e, Mul):
                    collect(e.left, power)
                    collect(e.right, power)
                elif isinstance(e, Pow):
                    if isinstance(e.right, Number):
                        collect(e.left, Number(power.value * e.right.value))
                    else:
                        factors[e] = Number(factors[e].value + power.value)
                else:
                    factors[e] = Number(factors[e].value + power.value)
            
            collect(expr)
            return coefficient, factors

        num_coeff, num_factors = get_factors(left_simple)
        den_coeff, den_factors = get_factors(right_simple)
        
        # Handle division of coefficients
        if den_coeff.value == 0:
            raise ZeroDivisionError("Division by zero")
        result_coeff = Number(num_coeff.value / den_coeff.value)
        
        # Cancel common factors
        for factor in list(num_factors.keys()):
            if factor in den_factors:
                min_power = min(num_factors[factor].value, den_factors[factor].value)
                num_factors[factor] = Number(num_factors[factor].value - min_power)
                den_factors[factor] = Number(den_factors[factor].value - min_power)
                
                if num_factors[factor].value == 0:
                    del num_factors[factor]
                if den_factors[factor].value == 0:
                    del den_factors[factor]
        
        # Reconstruct the result
        def build_expression(coeff, factors):
            result = None
            for base, power in sorted(factors.items(), key=lambda x: str(x[0])):
                term = base if power.value == 1 else Pow(base, power)
                result = term if result is None else Mul(result, term)
            return result if result is not None else Number(1)
        
        num_result = build_expression(Number(1), num_factors)
        den_result = build_expression(Number(1), den_factors)
        
        # Apply coefficient
        if result_coeff.value != 1:
            num_result = Mul(result_coeff, num_result)
        
        # If denominator is 1, return just the numerator
        if isinstance(den_result, Number) and den_result.value == 1:
            return num_result
            
        return Div(num_result, den_result)

    def __str__(self):
        return f"({self.left} / {self.right})"
    
