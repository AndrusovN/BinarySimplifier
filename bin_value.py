from variable_names import VariableNamesHolder
import gmpy2


# The basic class to store binary value - monom of Zhegalkin's Polynom
class BinValue:
    # data is a binary mask of variables, which are included in this monom
    # so if variable number i has non-zero power in this monom, (data >> i) & 1 is equal to 1
    # also can be known as ID of a monom
    data: int

    # included values - set of indexes of variables included to monom
    # data - the direct bitmask to initialize self.data - if this is None, direct initialization by data is used
    # otherwise, data is being initialized using included_values
    # if included_values is None and data is None - this is a simple monom - identical 1
    def __init__(self, included_values=None, data=None):
        if data is not None:
            self.data = data
            return
        if included_values is None:
            included_values = set()
        self.data = 0
        for e in included_values:
            self.data += 2**e

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)

    # the powers of variables included to monom can be accessed as binValue[i]
    def __getitem__(self, key) -> bool:
        return ((self.data >> key) & 1) == 1

    # count of variables with non-zero power in this monom
    def __len__(self):
        return gmpy2.popcount(self.data)

    # multiplication of monomes is just binary OR of their data fields
    def __mul__(self, other):
        return BinValue(data=(self.data | other.data))

    # make string from monom using variable names
    def __str__(self):
        current_value = self.data
        if current_value == 0:
            return "1"
        result = ""
        id = 0
        while current_value > 0:
            if current_value % 2 == 1:
                if len(result) > 0:
                    result += " * "
                result += VariableNamesHolder().get_variable_name(id)
            id += 1
            current_value = current_value // 2
        if gmpy2.popcount(self.data) > 1:
            result = f"({result})"
        return result
