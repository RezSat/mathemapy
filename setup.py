from mathemapy import *
x = Symbol('x')
y = Symbol('y')
num1 = Number(5)
num2 = Number(3)
expr = Subtraction(x, Subtraction(y, Subtraction(num1, num2))) # x - (y - (5 - 3)) -> x - (y - 2)
result = expr.evaluate()
print(result)
ep = Subtraction(Symbol('x'), Subtraction(Symbol('y'), Number(2)))
print(ep)
print(result == ep)

print(Subtraction(Number(-5), Symbol('y')))

print(ep)

print(Addition(Symbol('x'), Addition(Symbol('y'), Number(2))))