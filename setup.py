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

v = Multiplication(i, i)
l = v.evaluate()
print(v, '\n', l)
print(type(v), type(l))

print(Addition(v, v).evaluate())