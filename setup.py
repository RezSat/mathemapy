from mathemapy import *

x = Symbol('x')
y = Symbol('x')
expr = Multiplication(x, y)
result = expr.evaluate()

u = Power(Symbol('x'), Number(2))
print(result == u) # x * x = x^2
print(result)
print( u)
print(type(u.exponent) )
print(result.exponent)

p = Number(2)
print(p==2)