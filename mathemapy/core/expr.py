from abc import ABC, abstractmethod

class Expression(ABC):

    @abstractmethod
    def evaluate(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass