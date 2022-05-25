from singleton import singleton
from variable import Variable
from typing import *


@singleton
class VariableNamesHolder:
    variables: List[Variable]

    def __init__(self):
        self.variables = []

    def clear(self):
        for variable in self.variables:
            variable.id = -1
            del variable
        self.variables = []

    def get_variable(self, id: int) -> Variable:
        if 0 <= id < len(self.variables):
            return self.variables[id]
        else:
            raise Exception(f"Invalid variable id, should be in [{0}; {len(self.variables) - 1}], but {id} given")

    def get_variable_index(self, name: str) -> int:
        variables_with_requested_name = self.__get_variables_by_name(name)
        if len(variables_with_requested_name) == 0:
            raise Exception(f"No such variable registered: {name}")

        return variables_with_requested_name[0].id

    def __get_variables_by_name(self, name: str) -> List[Variable]:
        variables_with_requested_name = list(filter(
            lambda variable: variable.name == name,
            self.variables))

        return variables_with_requested_name

    def is_variable_registered(self, name: str) -> bool:
        variables_with_requested_name = self.__get_variables_by_name(name)

        return len(variables_with_requested_name) != 0

    # returns id of new registered variable
    def register_variable(self, variable: Variable) -> int:
        variable.id = len(self.variables)
        self.variables.append(variable)

        return len(self.variables) - 1

    def get_number_of_variables(self) -> int:
        return len(self.variables)
