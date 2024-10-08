
class Node:
    def is_node():
        return True

    def __eq__(self, other):
        return self._compare_same_type(other)

    def _compare_same_type(self, other):
        """This method should be overridden in subclasses for comparing objects of the same type."""
        raise NotImplementedError("Subclasses must implement this method for comparison")

    def __hash__(self):
        """Generate a hash based on the type and value of the object."""
        return hash((self.__class__, self._get_hash_value()))

    def _get_hash_value(self):
        """This method should be overridden to return the value to be hashed (e.g., the value of a number or symbol)."""
        raise NotImplementedError("Subclasses must implement this method for hashing")

    def evaluate(self,scope):
        """
        Evaluate the Node
        returns the result
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def __repr__(self):
        return self.__class__.__name__


