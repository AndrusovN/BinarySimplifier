# Holder of variables names
# This class works with given variables and processes their ids
from singleton import singleton


@singleton
class VariableNamesHolder:
    # List of variable name
    variable_names = []

    # Initialization with given list
    def __init__(self, variable_names = []):
        self.variable_names = variable_names

    # Gen name of variable by it's id
    def get_variable_name(self, id: int):
        if 0 <= id < len(self.variable_names):
            return self.variable_names[id]
        else:
            return None

    # Get variable index by name
    # Returns -1 if there is no such variable registered
    def get_variable_index(self, name: str):
        if name not in self.variable_names:
            return -1
        return self.variable_names.index(name)

    # Register a new variable
    def add_variable(self, name: str):
        self.variable_names.append(name)
        return len(self.variable_names) - 1
