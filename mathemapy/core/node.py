
class Node:
    def is_node():
        return True
    
    def evaluate(self,scope):
        """
        Evaluate the Node
        returns the result
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def __repr__(self):
        return self.__class__.__name__


