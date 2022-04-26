from parsing import parse
from variable_names import VariableNamesHolder
from sop_representation import SOPRepresentation


# initialize the Variable Names Holder
VariableNamesHolder([])
data = input()
polynom = parse(data)
# print the simplified value
print(str(polynom))
sop = SOPRepresentation(polynom)
sop.simplify_maximum()
print(str(sop))
