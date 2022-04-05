from bin_value import BinValue
from copy import deepcopy

from hashable_set import HashableSet
from or_block import OrBlock


# A class for storing Zhegalkin's polynom
class ZhegalkinsPolynom:
    # A set of BinValues (monoms) whose sum is the Zhegalkin's polynom
    values: set

    # Initialization with some values already given
    def __init__(self, values=None):
        if values is None:
            values = set()
        self.values = values

    # Sum of two polynoms
    def __add__(self, other):
        if type(other) == ZhegalkinsPolynom:
            return ZhegalkinsPolynom(self.values.symmetric_difference(other.values))
        elif type(other) == BinValue:
            return ZhegalkinsPolynom(self.values.symmetric_difference({other}))
        else:
            return None

    # Product of two polynoms
    def __mul__(self, other):
        result_set = set()
        for val1 in self.values:
            for val2 in other.values:
                res = val1 * val2
                if res in result_set:
                    result_set.remove(res)
                else:
                    result_set.add(res)
        return ZhegalkinsPolynom(result_set)

    # Check that the difference between polynoms is constant zero
    def __eq__(self, other):
        return len(self.values.symmetric_difference(other.values)) == 0

    # the OR operator of two polynoms
    def __or__(self, other):
        return self + other + (self * other)

    # Format polynom as string
    def __str__(self):
        # Generate the set of OrBlocks
        values_set = {OrBlock(binVal=item) for item in self.values}
        if len(values_set) == 0:
            return "0"
        result = ""
        # First of all unite everything in OrBlocks
        hasProgress = True
        while hasProgress:
            hasProgress = False
            tmp_values = [item for item in values_set]
            # tmp_values.sort(key=lambda x: len(x), reverse=True)
            # Iterate over all pair and try to unite them into one block
            for i in range(len(tmp_values)):
                for j in range(i + 1, len(tmp_values)):
                    # Try to unite
                    value = tmp_values[i] * tmp_values[j]
                    if value == tmp_values[i] or value == tmp_values[j]:
                        continue
                    # If success, unite and continue
                    if value in values_set:
                        nvalue = tmp_values[i] | tmp_values[j]
                        values_set.remove(value)
                        values_set.remove(tmp_values[i])
                        values_set.remove(tmp_values[j])
                        values_set.add(nvalue)
                        hasProgress = True
                        break
                if hasProgress:
                    break
        # Then print everything
        for value in values_set:
            if value.monoms_set.data == 1:
                continue
            if len(result) > 0:
                result += " ^ "
            result += str(value)
        if OrBlock(data=HashableSet(data=1)) in values_set:
            result = f"!({result})"
        return result
