def or_viceversa(this, other, this_i, other_i):
    # checks and return bool if two things  are of  some instance
    # ex: isisnstance (left, Number) and isinstance (right Symbol) and this checks the vice versa
    # if isinstance (right, Number) and isinstance (left, Symbol)
    return (isinstance(this, this_i) and isinstance(other, other_i) or 
    isinstance(this, other_i) and isinstance(other, this_i))