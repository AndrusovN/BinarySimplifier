from variable_names import VariableNamesHolder
import gmpy2
from hashable_set import HashableSet


# The basic class to store binary value - monom of Zhegalkin's Polynom
class BinValue:
    monom: HashableSet

    # included values - set of indexes of variables included to monom
    # data - the direct bitmask to initialize self.data - if this is None, direct initialization by data is used
    # otherwise, data is being initialized using included_values
    # if included_values is None and data is None - this is a simple monom - identical 1
    def __init__(self, included_values=None, data=None):
        if data is not None:
            self.monom = data
            return
        if included_values is None:
            included_values = set()
        self.monom = HashableSet(values=included_values)

    def __eq__(self, other):
        return self.monom == other.monom

    def __hash__(self):
        return hash(self.monom)

    # the powers of variables included to monom can be accessed as binValue[i]
    def __getitem__(self, key) -> bool:
        return self.monom[key]

    # count of variables with non-zero power in this monom
    def __len__(self):
        return len(self.monom)

    # multiplication of monomes is just binary OR of their data fields
    def __mul__(self, other):
        return BinValue(data=(self.monom | other.monom))

    # make string from monom using variable names
    def __str__(self):
        if len(self.monom) == 0:
            return "1"
        result = ""
        for variable in self.monom:
            if len(result) > 0:
                result += " * "
            result += VariableNamesHolder().get_variable_name(variable)
        if len(self.monom) > 1:
            result = f"({result})"
        return result
