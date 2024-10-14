here are some of the basic things that i understood in working
with this project,

negation should be native instead of a separate negation class
we actually don't need operator types such as binary, unary etc
stop thinking that this software is for babies, it's not so dont' hesitate to build more advanced features and we don't need to explain each an every simple details.

basic operations should be able to handle multople inputs not jsut left and right two arguments

ex: Add(1,2) but also Add(1,2,3,3) not just Add(left, right) 
same goes for other operators

and this should also be possible -Add(1,2) -> -3
instead of doing Negate(Add(1,2)) well we could have a separte negate object but that should also support natively not just for operators but also for Atoms such as  Number, Symbol

also Number, Symbol should also support native arithmentic instead

like Number(2) + Number(2).

instead of using int, float always use  Integer , Float which are custom build classes to this CAS this will make it much easier to keep the code to a standard as well.

isntead of creating BinaryOperator, UnaryOperator like class use the approach like Sympy or Math.JS and just create a single Operator class which can expect any number of arguments or Expression classes which can handle overall things, and Atom classes for singles.

need some more research on those.
we cannot just straight up copy the structure of sympy since our system build for pedagogy purposes.


rewriting  the same software multiple times is just super frustating but also hyper fun at the same time

HAHHAHAHHAHAHAHAHA.

the idea so he is that the system of things being the same as fucking hell so i can easliy set the hyper lander space to keep the soft copy of the shit cooling