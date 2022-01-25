from bin_value import BinValue


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

    def __or__(self, other):
        return self + other + (self * other)

    def __str__(self):
        if len(self.values) == 0:
            return "0"
        result = ""
        for value in self.values:
            if len(result) > 0:
                result += " ^ "
            result += str(value)
        return result
