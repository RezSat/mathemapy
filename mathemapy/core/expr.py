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

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

