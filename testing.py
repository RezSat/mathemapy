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

class LikeTerms():
    def __init__(self, _dict):
        self.__dict__.update(_dict)

    @property
    def terms(self):
        return list(self.__dict__.keys())

    def _is_there(self, term):
        return True if term in self.terms else False

    def __repr__(self):
        return str(self.__dict__)

class Subtraction(BinaryOperator):
    symbol = '-'

    def evaluate(self):
        e_left = self.left.evaluate() if not isinstance(self.left, Symbol) else self.left
        e_right = self.right.evaluate() if not isinstance(self.right, Symbol) else self.right


        if isinstance(e_left, (int, float)) and isinstance(e_right, (int, float)):
            return Number(e_left - e_right)

        if isinstance(e_right, LikeTerms):
            if e_right._is_there()
        return self._collect_like_terms(e_left, e_right)

    def _collect_like_terms(self, *terms):
        collectd = {}
        for term in terms:
            if isinstance(term, Symbol):
                # collect symbols
                if term.name  in collectd:
                    collectd[term.name] -= 1 # Decrease the coefficient
                else:
                    collectd[term.name] = 1
            
        result = []
        for term, coeff in collectd.items():
            if coeff == 0:
                result.append(Number(0))
            elif coeff == 1:
                result.append(Symbol(term))
            else:
                result.append(Multiplication(Number(coeff), Symbol(term)))

        return LikeTerms(collectd)
                



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


here is  an idea:

create a separate  class to hold like terms, symbols and it's coefficient values
then use this under recursion to determine similar terms in nested subs as this object now
can be passed easily through out the tree with just instance recognition unlike recognizing
of dicts since this is a separate class there won't be any mismatch when checking 
for instances even in the future expansions.


"""


#result = expr.evaluate()
#print(result)
#ep = Subtraction(Symbol('x'), Subtraction(Symbol('y'), Number(2)))
#print(ep)
#print(result == ep)

#print(Subtraction(Number(-5), Symbol('y')))


#print(Addition(Symbol('x'), Addition(Symbol('y'), Number(2))))

