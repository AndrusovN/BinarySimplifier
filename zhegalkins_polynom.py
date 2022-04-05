from bin_value import BinValue
from copy import deepcopy
from or_block import OrBlock


class ZhegalkinsPolynom:
    values: set

    def __init__(self, values=None):
        if values is None:
            values = set()
        self.values = values

    def __add__(self, other):
        if type(other) == ZhegalkinsPolynom:
            return ZhegalkinsPolynom(self.values.symmetric_difference(other.values))
        elif type(other) == BinValue:
            return ZhegalkinsPolynom(self.values.symmetric_difference(set([other])))
        else:
            return None

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

    def __eq__(self, other):
        return len(self.values.symmetric_difference(other.values)) == 0

    def __or__(self, other):
        return self + other + (self * other)

    def __str__(self):
        values_set = {OrBlock(binVal=item) for item in self.values}

        if len(values_set) == 0:
            return "0"
        result = ""

        hasProgress = True
        while hasProgress:
            hasProgress = False
            tmp_values = [item for item in values_set]
            # tmp_values.sort(key=lambda x: len(x), reverse=True)
            for i in range(len(tmp_values)):
                for j in range(i + 1, len(tmp_values)):
                    value = tmp_values[i] * tmp_values[j]
                    if value.data == tmp_values[i].data or value.data == tmp_values[j].data:
                        continue
                    if value in values_set:
                        nvalue = OrBlock(orBlock1=tmp_values[i], orBlock2=tmp_values[j])
                        values_set.remove(value)
                        values_set.remove(tmp_values[i])
                        values_set.remove(tmp_values[j])
                        values_set.add(nvalue)
                        hasProgress = True
                        break
                if hasProgress:
                    break

        for value in values_set:
            if value.data == 1:
                continue
            if len(result) > 0:
                result += " ^ "
            result += str(value)
        if OrBlock(data=1) in values_set:
            result = f"!({result})"
        return result
