from mathemapy import *

x = Number(1)
y = Number(2)
m = Float(2.3, preceision=2)
p = Float(4.5, preceision=2)
i = Symbol('x')
o = Symbol('x')
q = Symbol('y')
z = Addition(m,o)
u = z.evaluate()
print(i==o)
print(z, u)

x = Symbol('x')
y = Symbol('y')
num1 = Number(5)
num2 = Number(3)

# Add two numbers
expr = Addition(num1, num2)
print(expr.evaluate())  # Output: Number(8)

# Add two symbols and a number
expr = Addition(x, Addition(x, Addition(num1, Addition(q, num2))))
print(expr.evaluate())  # Output: (x + y + 5)
print(expr.terms)

# Complex case: x + 2*x + 3 + x
x = Symbol('x')
y = Symbol('2x')
num1 = Number(5)
num2 = Number(3)
expr = Addition(x,y )
print(expr.evaluate())  # Output: (4*x + 3)
print(expr.terms)