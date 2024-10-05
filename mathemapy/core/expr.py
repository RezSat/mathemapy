class Expr:
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._compare_same_type(other)
        return False

    def _compare_same_type(self, other):
        """This method should be overridden in subclasses for comparing objects of the same type."""
        raise NotImplementedError("Subclasses must implement this method for comparison")

    def __hash__(self):
        """Generate a hash based on the type and value of the object."""
        return hash((self.__class__, self._get_hash_value()))

    def _get_hash_value(self):
        """This method should be overridden to return the value to be hashed (e.g., the value of a number or symbol)."""
        raise NotImplementedError("Subclasses must implement this method for hashing")

    def __repr__(self):
        """This method should return a string representation of the object."""
        raise NotImplementedError("Subclasses must implement this method for representation")
