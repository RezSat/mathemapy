from abc import ABC, abstractmethod
from typing import Union

class Expression(ABC):
    
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def simplify(self):
        pass