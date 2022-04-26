from hashable_set import HashableSet
from variable_names import VariableNamesHolder


class AndBlock:
    straight_values: HashableSet
    inversed_values: HashableSet

    def __init__(self, straight_values=HashableSet(), inversed_values=HashableSet()):
        self.straight_values = straight_values
        self.inversed_values = inversed_values

    def try_match(self, other):
        straight = self.straight_values ^ other.straight_values
        inverse = self.inversed_values ^ other.inversed_values
        if len(straight) != 1:
            return None
        if straight != inverse:
            return None

        straight_result = (self.straight_values | other.straight_values) ^ straight
        inverse_result = (self.inversed_values | other.inversed_values) ^ inverse

        return straight_result, inverse_result

    def __hash__(self):
        return hash(self.straight_values) * 179 + hash(self.inversed_values)

    def __eq__(self, other):
        return self.inversed_values == other.inversed_values and self.straight_values == other.straight_values

    def is_subset(self, other):
        return self.inversed_values.is_subset(other.inversed_values) and \
               self.straight_values.is_subset(other.straight_values)

    def __str__(self):
        result = ""
        for item in self.straight_values:
            if len(result) > 0:
                result += ' * '
            result += VariableNamesHolder().get_variable_name(item)
        for item in self.inversed_values:
            if len(result) > 0:
                result += ' * '
            result += f'(!{VariableNamesHolder().get_variable_name(item)})'
        return result
