from mathemapy import (
    BinaryOperator,
    Number,
    Symbol,
    Node,
    Multiplication,
    Negate,
    or_viceversa,
    Addition
)
x = Symbol('x')
y = Symbol('y')
num1 = Number(5)
num2 = Number(3)

class Subtraction(BinaryOperator):
    symbol = '-'

    def evaluate(self):
        e_left = self.left.evaluate() if not isinstance(self.left, Symbol) else self.left
        e_right = self.right.evaluate() if not isinstance(self.right, Symbol) else self.right

        if isinstance(e_left, (int, float, Number)) and isinstance(e_right, (int, float, Number)):
            return Number(e_left - e_right)

        

        return Addition(e_left, Negate(e_right))



expr = Subtraction(x, Subtraction(x, Subtraction(num1, num2))) # x - (y - (5 - 3)) -> x - (y - 2)
print(expr)
print(expr.evaluate())
"""

so the idea  is to subtract these at once:

5 - 6 -6 -7 -2 -x
 and not convert this into sub(5, sub(6, sub(6, sub(7, sub(2,x)))))

instead make this flattern and collect the like terms into  one and subtract this all at once
like so : [5,-6,-6. -7-2] and [-x]
this would make it really easy  to subtract and no need to wait 

if this was the case sub(5, sub(6, sub(6, sub(7, sub(2,x))))):
    then the simplification steps would look something like this:

    5-6-6-7-2-x
    -1-6-7-2-x
    -7-7-2-x
    -14-2-x
    -16-x

but i would like this to be straight forward and do this -16-x straight up?  or is the above look nice?
for pedagogy

or as wolframalpha  like to do  

5-6-6-7-2-x
-x + 5 -(6+6+7+2)
-x +5 -(21)
-x  - 16
-(x+16)

so i guess implement several ways  of handling this ? yeah, but we need a default way to go as well
right? so so sos wht should i  dooooooooo
as if we were to implement the version fom WL then would need to implement factorization and all
but we still don' have those so i guess for now stick to the above 



okay let's not flattern straight away sicne this would make some expressions loose its structure
so let's just stick with nested subs

well then arisses a little problem which is this:

3-2-x so 
sub(3,sub(2,x))
right doesn't get evaluated?
so we need to do the collect like terms and bunch of other stuffs

"""


#result = expr.evaluate()
#print(result)
#ep = Subtraction(Symbol('x'), Subtraction(Symbol('y'), Number(2)))
#print(ep)
#print(result == ep)

#print(Subtraction(Number(-5), Symbol('y')))


#print(Addition(Symbol('x'), Addition(Symbol('y'), Number(2))))

