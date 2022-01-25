from singleton import singleton


@singleton
class VariableNamesHolder:
    variable_names = []

    def __init__(self, variable_names):
        self.variable_names = variable_names

    def get_variable_name(self, id: int):
        if 0 <= id < len(self.variable_names):
            return self.variable_names[id]
        else:
            return None

    def get_variable_index(self, name: str):
        if name not in self.variable_names:
            return -1
        return self.variable_names.index(name)

    def add_variable(self, name: str):
        self.variable_names.append(name)
        return len(self.variable_names) - 1
