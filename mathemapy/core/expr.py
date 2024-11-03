from abc import ABC, abstractmethod

class Expression(ABC):

    """
    Expression class will be the parent for all other classes.
    """

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def simplify(self):
        pass

    def __eq__(self, other: 'Expression') -> bool:
        if not isinstance(other, Expression):
            return False

        # Compare simplified forms
        return str(self.simplify()) == str(other.simplify())

    def __hash__(self):
        return hash(str(self.simplify()))

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

