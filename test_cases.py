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
        
        def collect_terms(expr):
            """Recursively collect terms from nested additions"""
            if isinstance(expr, Add):
                collect_terms(expr.left)
                collect_terms(expr.right)
            else:
                add_term(expr)
        
        def add_term(expr, coefficient=Number(1)):
            if isinstance(expr, Number):
                terms[Number(1)] = Number(terms[Number(1)].value + expr.value)
            elif isinstance(expr, Symbol):
                terms[expr] = Number(terms[expr].value + coefficient.value)
            elif isinstance(expr, Mul):
                # Handle cases like 2*x + 3*x
                if isinstance(expr.left, Number) and isinstance(expr.right, Symbol):
                    terms[expr.right] = Number(terms[expr.right].value + expr.left.value)
                elif isinstance(expr.right, Number) and isinstance(expr.left, Symbol):
                    terms[expr.left] = Number(terms[expr.left].value + expr.right.value)
                else:
                    terms[expr] = Number(terms[expr].value + coefficient.value)
            else:
                terms[expr] = Number(terms[expr].value + coefficient.value)
        
        # Collect terms from both sides
        collect_terms(left_simple)
        collect_terms(right_simple)
        
        # Construct the simplified expression
        result = None
        sorted_terms = sorted(terms.items(), key=lambda x: str(x[0]))  # Sort terms for consistent output
        
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
        
        # If both operands are numbers, compute the result
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            return Number(left_simple.value * right_simple.value)
        
        # If either operand is zero, return zero
        if (isinstance(left_simple, Number) and left_simple.value == 0) or \
           (isinstance(right_simple, Number) and right_simple.value == 0):
            return Number(0)
        
        # If either operand is one, return the other operand
        if isinstance(left_simple, Number) and left_simple.value == 1:
            return right_simple
        if isinstance(right_simple, Number) and right_simple.value == 1:
            return left_simple
        
        return Mul(left_simple, right_simple)

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
        
        if isinstance(right_simple, Number) and right_simple.value == 0:
            raise ZeroDivisionError("Division by zero")
        
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            return Number(left_simple.value / right_simple.value)
        
        return Div(left_simple, right_simple)

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
        
        if isinstance(left_simple, Number) and isinstance(right_simple, Number):
            return Number(left_simple.value ** right_simple.value)
        
        # x^0 = 1
        if isinstance(right_simple, Number) and right_simple.value == 0:
            return Number(1)
        
        # x^1 = x
        if isinstance(right_simple, Number) and right_simple.value == 1:
            return left_simple
        
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