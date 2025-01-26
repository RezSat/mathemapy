from core import *
import math

x = Symbol('x')
y =  Symbol('y')
expr1 = Number(1) + Number(2)
print(expr1.simplify()) # 3

expr2 = Number(1) + x
print(expr2.simplify()) # x + 1

expr3 = x + x
print(expr3)
print(expr3.simplify()) # 2*x

# 2*(x*y) + 3*(x*y)
expr4 = Number(2) * x * y + Number(3) * x * y
print(expr4)
print(expr4.simplify())

sin = Function('sin', [Symbol('x')], math.sin)

expr1 = sin(x)
print(expr1)

pi = Number(math.pi)
expr2 = sin(pi / Number(2))
print(expr2.simplify())

expr3 = sin(x + y)
print(expr3)