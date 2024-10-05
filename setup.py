from mathemapy import *

x = Symbol('x')
y = Symbol('x')
expr = Multiplication(x, y)
result = expr.evaluate()
print(result == Power(Symbol('x'), Number(2))) # x * x = x^2
print(result)
print( Power(Symbol('x'), Number(2)))
print(expr)