from parsing import parse
from variable_names import VariableNamesHolder

# initialize the Variable Names Holder
VariableNamesHolder([])
data = input()
# print the simplified value
print(str(parse(data)))
