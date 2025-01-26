from .numbers import Number
from .expr import Expression
from typing import List, Callable

class Function(Expression):
    def __init__(self, name: str, args: List[Expression], func: Callable = None):
        self.name = name
        self.args = args
        self.func = func

    def evaluate(self):
        if self.func:
            return self.func(*[arg.evaluate() for arg in self.args])
        return self # if no function is defined return the symbolic representation
    
    def simplify(self):
        simpliified_args = [ arg.simplify() for arg in self.args ]
        if all(isinstance(arg, Number) for arg in simpliified_args) and self.func:
            return Number(self.func(*[arg.value for arg in simpliified_args]))
        return Function(self.name, simpliified_args, self.func)
    
    def __call__(self, *args):
        """
        makes the funciton object callable, but does not simplify or evaluate the result
        for that call those respective methods on the called function object
        ex: sin(pi/2) -> sin(pi/2) but sin(pi/2).simplify() -> 1
        
        """

        if len(args) != len(self.args):
            raise ValueError(f"{self.name} expects {len(self.args)} arguments, but got {len(args)}")
        return Function(self.name, list(args), self.func)
    
    def alternative(self):
        return self
    
    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.args)
        return f"{self.name}({args_str})"
    
    def __eq__(self, other):
        return (isinstance(other, Function) and 
                self.name == other.name and 
                self.args == other.args)
    
    def __hash__(self):
        return hash((self.name, tuple(self.args)))