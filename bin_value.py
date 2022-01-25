from variable_names import VariableNamesHolder


class BinValue:
    data: int

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

    def __getitem__(self, key) -> bool:
        return ((self.data >> key) & 1) == 1

    def __mul__(self, other):
        return BinValue(data=(self.data | other.data))

    def __str__(self):
        current_value = self.data
        if current_value == 0:
            return "1"
        result = ""
        id = 0
        while current_value > 0:
            if current_value % 2 == 1:
                if len(result) > 0:
                    result += "*"
                result += VariableNamesHolder().get_variable_name(id)
            id += 1
            current_value = current_value // 2
        return result
