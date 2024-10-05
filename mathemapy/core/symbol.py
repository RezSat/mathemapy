from .node import Node

class Symbol(Node):
    is_Symbol = True
    is_symbol = True

    def __init__(self, name, **assumptions):
        self.name = name
        self.assumptions = self._sanitize(assumptions)

    def _get_hash_value(self):
        return self.name

    def _compare_same_type(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.__class__, self._get_hash_value()))

    def evaluate(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def _sanitize(assumptions):
        """
        Sanitize assumptions such as commutative, real, positive, integer.
        """
        valid_assumptions = {'commutative', 'real', 'positive', 'integer'}
        sanitzed_assumptions = {}
        for key, value in assumptions.items():
            if key in valid_assumptions:
                sanitzed_assumptions[key] = bool(value)
        sanitzed_assumptions.setdefault('commutative', True)
        return sanitzed_assumptions

    def is_real(self):
        return self.assumptions.get('real', None)

    def is_positive(self):
        return self.assumptions.get('positive', None)
    
    def is_integer(self):
        return self.assumptions.get('integer', None)

    def is_commutative(self):
        return self.assumptions.get('commutative', True)

class Dummy(Symbol):
    _count = 0 # Internal counter to ensure uniqueness

    def __init__(self, name=None, **assumptions):
        if name is None:
            name =f"Dummy_{Dummy._count}"
        Dummy._count += 1
        super().__init__(name, **assumptions)

class Wild(Symbol):
    def __init__(self, name, exclude=(), **assumptions):
        super().__init__(name, **assumptions)
        self.exclude = exclude

    def matches(self,expr):
        # Basic pattern matching  logic
        if any(e in expr for e in self.exclude):
            return None
        return {self:expr}