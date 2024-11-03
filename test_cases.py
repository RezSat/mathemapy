from abc import ABC, abstractmethod
from typing import Union, List, Dict
from collections import defaultdict

class Expression(ABC):
    """
    Expression class is the parent for all other classes
    """
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def simplify(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)

class Add(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left + eval_right)
        
        return self.simplify()
    
    def simplify(self):
        left_simple = self.left.simplify()
        right_simple = self.right.simplify()
        
        # If both operands are numbers, compute the result
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            return Number(left_simple.value + right_simple.value)
        
        # Combine like terms
        terms = defaultdict(lambda: Number(0))
        
        def get_canonical_form(expr):
            """Get a canonical string representation for comparison"""
            if isinstance(expr, Mul):
                factors = []
                coefficient = Number(1)
                
                def collect_factors(e):
                    nonlocal coefficient
                    if isinstance(e, Number):
                        coefficient = Number(coefficient.value * e.value)
                    elif isinstance(e, Mul):
                        collect_factors(e.left)
                        collect_factors(e.right)
                    else:
                        factors.append(str(e))
                
                collect_factors(expr)
                factors.sort()
                return tuple(factors), coefficient
            return (str(expr),), Number(1)
        
        def collect_terms(expr, coeff=Number(1)):
            if isinstance(expr, Add):
                collect_terms(expr.left)
                collect_terms(expr.right)
            else:
                canonical_form, term_coeff = get_canonical_form(expr)
                total_coeff = Number(coeff.value * term_coeff.value)
                terms[canonical_form] = Number(terms[canonical_form].value + total_coeff.value)
        
        # Collect terms from both sides
        collect_terms(left_simple)
        collect_terms(right_simple)
        
        # Construct the simplified expression
        result = None
        sorted_terms = sorted(terms.items())  # Sort terms for consistent output
        
        def reconstruct_term(canonical_form):
            """Reconstruct term from canonical form"""
            if len(canonical_form) == 1:
                # Single term
                if isinstance(left_simple, Symbol) and str(left_simple) == canonical_form[0]:
                    return left_simple
                if isinstance(right_simple, Symbol) and str(right_simple) == canonical_form[0]:
                    return right_simple
                # Search in multiplicative terms
                if isinstance(left_simple, Mul) and str(left_simple) == canonical_form[0]:
                    return left_simple
                if isinstance(right_simple, Mul) and str(right_simple) == canonical_form[0]:
                    return right_simple
            else:
                # Multiplicative term
                term = None
                for factor_str in canonical_form:
                    factor = None
                    # Try to find the original expression for this factor
                    if isinstance(left_simple, Symbol) and str(left_simple) == factor_str:
                        factor = left_simple
                    elif isinstance(right_simple, Symbol) and str(right_simple) == factor_str:
                        factor = right_simple
                    
                    if factor is None:
                        # Search in multiplicative terms
                        if isinstance(left_simple, Mul):
                            if str(left_simple.left) == factor_str:
                                factor = left_simple.left
                            elif str(left_simple.right) == factor_str:
                                factor = left_simple.right
                        if isinstance(right_simple, Mul):
                            if str(right_simple.left) == factor_str:
                                factor = right_simple.left
                            elif str(right_simple.right) == factor_str:
                                factor = right_simple.right
                    
                    if factor is not None:
                        term = factor if term is None else Mul(term, factor)
                
                return term
        
        for canonical_form, coeff in sorted_terms:
            if coeff.value == 0:
                continue
            
            term = reconstruct_term(canonical_form)
            if term is not None:
                if coeff.value != 1:
                    term = Mul(Number(coeff.value), term)
                
                if result is None:
                    result = term
                else:
                    result = Add(result, term)
        
        return result if result is not None else Number(0)
        
    def __str__(self):
        return f"({self.left} + {self.right})"

class Sub(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        return Add(self.left, Mul(Number(-1), self.right)).evaluate()
    
    def simplify(self):
        return Add(self.left, Mul(Number(-1), self.right)).simplify()

    def __str__(self):
        return f"({self.left} - {self.right})"
    
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
            terms = []
            coefficient = Number(1)
            
            def collect_factors(expr):
                """Recursively collect factors, maintaining their structure"""
                nonlocal coefficient
                
                if isinstance(expr, Number):
                    coefficient = Number(coefficient.value * expr.value)
                elif isinstance(expr, Mul):
                    collect_factors(expr.left)
                    collect_factors(expr.right)
                else:
                    terms.append(expr)
            
            # Collect all factors
            collect_factors(left_simple)
            collect_factors(right_simple)
            
            # If coefficient is 0, return 0
            if coefficient.value == 0:
                return Number(0)
            
            # Sort terms for canonical form
            # Convert terms to strings for sorting to ensure consistent ordering
            terms.sort(key=lambda x: str(x))
            
            # Reconstruct the expression
            result = None
            
            # Combine like terms
            i = 0
            while i < len(terms):
                current_term = terms[i]
                count = 1
                j = i + 1
                
                # Look ahead for identical terms
                while j < len(terms) and str(terms[j]) == str(current_term):
                    count += 1
                    j += 1
                
                # Add the term with its power if necessary
                term = current_term if count == 1 else Pow(current_term, Number(count))
                
                if result is None:
                    result = term
                else:
                    result = Mul(result, term)
                
                i = j
            
            if result is None:
                return coefficient
            
            return result if coefficient.value == 1 else Mul(coefficient, result)

    def __str__(self):
        return f"({self.left} * {self.right})"

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
    
class Pow(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self):
        eval_left = self.left.evaluate()
        eval_right = self.right.evaluate()

        if isinstance(eval_left, (int, float)) and isinstance(eval_right, (int, float)):
            return Number(eval_left ** eval_right)

        return self.simplify()
    
    def simplify(self):
        left_simple = self.left.simplify()
        right_simple = self.right.simplify()
        
        # Handle numeric powers
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            return Number(left_simple.value ** right_simple.value)
        
        # x^0 = 1
        if isinstance(right_simple, Number) and right_simple.value == 0:
            return Number(1)
        
        # x^1 = x
        if isinstance(right_simple, Number) and right_simple.value == 1:
            return left_simple
        
        # Handle nested powers: (x^a)^b = x^(a*b)
        if isinstance(left_simple, Pow):
            new_exp = Mul(left_simple.right, right_simple).simplify()
            return Pow(left_simple.left, new_exp).simplify()
        
        # 1^x = 1
        if isinstance(left_simple, Number) and left_simple.value == 1:
            return Number(1)
        
        return Pow(left_simple, right_simple)

    def __str__(self):
        return f"({self.left} ^ {self.right})"
        
class Number(Expression):
    def __init__(self, value: Union[int, float]):
        self.value = value

    def evaluate(self):
        return self.value
    
    def simplify(self):
        return self
    
    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        return False
    
    def __hash__(self):
        return hash(self.value)
    
    def __str__(self):
        return f"{self.value}"

class Symbol(Expression):
    def __init__(self, name: str):
        self.name = name

    def evaluate(self):
        return self

    def simplify(self):
        return self
    
    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return f"{self.name}"
    

print("Edge Cases in Expression Handling:")

# These cases might not be handled properly:
x = Symbol('x')
y = Symbol('y')

# Test negative numbers and their simplification
expr1 = Number(-2) * x + Number(-3) * x
print(expr1.simplify())  # Should give (-5 * x)

# Multiple negations
expr2 = Number(-1) * (Number(-1) * x)
print(expr2.simplify())  # Should give x

# Zero handling in multiplication
expr3 = Number(0) * (x + y)
print(expr3.simplify())  # Should give 0

# Power of zero handling
expr4 = Pow(x, Number(0))
print(expr4.simplify())  # Should give 1

# Division by expressions containing zero
expr5 = x / (y - y)
# Should raise ZeroDivisionError when simplified
try:
    expr5.simplify()
except ZeroDivisionError:
    print("ZeroDivisionError")


print("\n\nAssociativity Issues:")

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

# These expressions should give equivalent results but might not:
expr1 = (x + y) + z
expr2 = x + (y + z)
print(expr1.simplify())
print(expr2.simplify())

# Same for multiplication
expr3 = (x * y) * z
expr4 = x * (y * z)
print(expr3.simplify())
print(expr4.simplify())

print("\n\nCommutativity in Terms:")

x = Symbol('x')
y = Symbol('y')

# These should simplify to the same expression:
expr1 = x * y + y * x
print(expr1.simplify())  # Should combine like terms, but result is : ((x * y) + (x * y))

expr2 = Number(2) * x * y + y * x * Number(3)
print(expr2.simplify())  # Should give (5 * x * y), but result is : (2 * (x * y)) + (3 * (x * y)))


print("\n\nComplex Fraction Handling:")

x = Symbol('x')
y = Symbol('y')

# Complex fraction simplification
expr1 = (x/y) / (y/x)
print(expr1.simplify())  # Should give (x^2 / y^2), but result is: ((x / y) / (y / x))

# Multiple divisions
expr2 = x / y / z
print(expr2.simplify())  # Should handle proper association, the result  is : ((x / y) / z)

# Division of sums
expr3 = (x + y) / (x + y)
print(expr3.simplify())  # Should give 1


print("\n\nPower Simplification Edge Cases:")

x = Symbol('x')
y = Symbol('y')

# Power of power simplification
expr1 = Pow(Pow(x, Number(2)), Pow(y, Number(2)))
print(expr1.simplify())  # Should handle nested powers, result is: (x ^ (2 * (y ^ 2)))

# Power distribution
expr2 = Pow(x * y, Number(2))
print(expr2.simplify())  # Should give (x^2 * y^2), but result is: ((x * y) ^ 2) maybe this is okay, but add some method like `alternaive` so that the other result will also can be print.

# Zero base with positive exponent
expr3 = Pow(Number(0), Number(5))
print(expr3.simplify())  # Should give 0

# Zero base with zero exponent
expr4 = Pow(Number(0), Number(0))
print(expr4.simplify())  # Should be undefined or raise an error, but result gives: 1


print("\n\nError Handling Improvements:")
x = Symbol('x')

# Division by zero in more complex expressions
expr1 = x / (x - x)  # Should raise ZeroDivisionError
try:
    expr1.simplify()
except ZeroDivisionError:
    print("ZeroDivisionError")

# Undefined mathematical operations
expr2 = Pow(Number(0), Number(-1))  # Should raise appropriate error
try:
    expr2.simplify()
except ZeroDivisionError:
    print("ZeroDivisionError: 0.0 cannot be raised to a negative power")

# Invalid operations
expr3 = Pow(x, Number(1/2))  # How should fractional powers be handled?
print(expr3.simplify()) # current output is (x ^ 0.5) ?? need to think how this shouild be handled, or we can also implement `alternative` method here as well so that it can output in other alternative formats like using fractional powers, root sign etc.


print('\n\nConsistent String Representation:')
x = Symbol('x')
y = Symbol('y')

# Consistent parentheses usage
expr1 = (x + y) * x
expr2 = x * (x + y)
print(expr1)  # Should have consistent parentheses placement
print(expr2)

# Number representation
expr3 = Number(1.0) * x  # Should it print as 1 or 1.0?
print(expr3) # curretly prints 1.0

# Complex expression formatting
expr4 = (x + y) * (x - y) / (x * y)
print(expr4)  # Should be readable and unambiguous, output is : (((x + y) * (x - y)) / (x * y))






# Test cases
x = Symbol('x')
expr1 = x + x  # Should simplify to 2x
print(expr1.simplify())  # Output: (2 * x)

expr2 = Number(2) * x + Number(3) * x  # Should simplify to 5x
print(expr2.simplify())  # Output: (5 * x)

x = Symbol('x')

# Test case 1: Simple addition of like terms
expr1 = x + x
print(f"x + x = {expr1.simplify()}")  # Should output: (2 * x)

# Test case 2: Addition with coefficients
expr2 = Number(2) * x + Number(3) * x
print(f"2x + 3x = {expr2.simplify()}")  # Should output: (5 * x)

# Test case 3: Mixed terms with constants
expr3 = x + Number(2) + x + Number(3)
print(f"x + 2 + x + 3 = {expr3.simplify()}")  # Should output: ((2 * x) + 5)

# Additional test cases
expr4 = Number(2) * x + Number(3) + x + Number(2)
print(f"2x + 3 + x + 2 = {expr4.simplify()}")  # Should output: ((3 * x) + 5)

expr5 = Number(2) * x + Number(3) * x + Number(4) + Number(1)
print(f"2x + 3x + 4 + 1 = {expr5.simplify()}")  # Should output: ((5 * x) + 5)

x = Symbol('x')
y = Symbol('y')

# Test multiplication simplification
test1 = (Number(2) * x) * (Number(3) * x)
print(f"(2x)(3x) = {test1.simplify()}")  # Should output: (6 * (x ^ 2))

test2 = x * y * x
print(f"x*y*x = {test2.simplify()}")  # Should output: ((x ^ 2) * y)

# Test division simplification
test3 = (Number(2) * x * y) / (x * Number(2))
print(f"(2xy)/(2x) = {test3.simplify()}")  # Should output: y

# Test power simplification
test4 = Pow(Pow(x, Number(2)), Number(3))
print(f"(x^2)^3 = {test4.simplify()}")  # Should output: (x ^ 6)

test5 = (x * x * y) / (x * y)
print(f"(x*x*y)/(x*y) = {test5.simplify()}")  # Should output: x, 

