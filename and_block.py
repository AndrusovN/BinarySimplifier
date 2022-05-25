from hashable_set import HashableSet
from variable_names import VariableNamesHolder


class AndBlock:
    required_true_variables: HashableSet
    required_false_variables: HashableSet

    def __init__(self, straight_values=HashableSet(), inversed_values=HashableSet()):
        self.required_true_variables = straight_values
        self.required_false_variables = inversed_values

    def try_match(self, other):
        straight = self.required_true_variables ^ other.required_true_variables
        inverse = self.required_false_variables ^ other.required_false_variables
        if len(straight) != 1:
            return None
        if straight != inverse:
            return None

        straight_result = (self.required_true_variables | other.required_true_variables) ^ straight
        inverse_result = (self.required_false_variables | other.required_false_variables) ^ inverse

        return straight_result, inverse_result

    def __hash__(self):
        return hash(self.required_true_variables) * 179 + hash(self.required_false_variables)

    def __eq__(self, other):
        return self.required_false_variables == other.required_false_variables and self.required_true_variables == other.required_true_variables

    def is_subset(self, other):
        return self.required_false_variables.is_subset(other.required_false_variables) and \
               self.required_true_variables.is_subset(other.required_true_variables)

    def contains(self, variable_id: int, negation=False):
        if negation:
            return self.required_false_variables[variable_id]
        else:
            return self.required_true_variables[variable_id]

    def deepcopy(self):
        return AndBlock(self.required_true_variables.deepcopy(), self.required_false_variables.deepcopy())

    def remove_variable(self, variable_id: int, negation=False):
        if negation:
            self.required_false_variables.remove(variable_id)
            return self
        else:
            self.required_true_variables.remove(variable_id)
            return self

    def __str__(self):
        result = ""
        for item in self.required_true_variables:
            if len(result) > 0:
                result += ' * '
            result += VariableNamesHolder().get_variable_name(item)
        for item in self.required_false_variables:
            if len(result) > 0:
                result += ' * '
            result += f'(!{VariableNamesHolder().get_variable_name(item)})'
        return result
