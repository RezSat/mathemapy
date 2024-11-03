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
