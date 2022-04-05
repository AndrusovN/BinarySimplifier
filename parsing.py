from zhegalkins_polynom import ZhegalkinsPolynom
from bin_value import BinValue
from variable_names import VariableNamesHolder


# Function to apply operator op to polynoms polynom1 and polynom2
# polynom1 and polynom2 are Zhegalkin's polynoms
# op is string with polynom
def resolve_op(polynom1, polynom2, op):
    if op == '*':
        return polynom1 * polynom2
    elif op == '+':
        return polynom1 | polynom2
    elif op == '^':
        return polynom1 + polynom2
    else:
        print(f'unknown operator {op}')
        return None


# The main parsing function
def parse(data: str) -> ZhegalkinsPolynom:
    data = data.replace(' ', '')
    if len(data) == 0 or data == "0":
        return ZhegalkinsPolynom()
    if data == "1":
        return ZhegalkinsPolynom(values=set(BinValue()))
    if data[0] == '!':
        return parse(data[1:]) + BinValue()
    # If data starts with bracket, solve the first part (inside bracket) and then the second part
    if data[0] == '(':
        brackets_balance = 1
        index = 1
        # calculate brackets balance
        while brackets_balance > 0 and index < len(data):
            if data[index] == ')':
                brackets_balance -= 1
            elif data[index] == '(':
                brackets_balance += 1
            index += 1
        if brackets_balance > 0:
            print("ERROR while parsing - brackets balance is not 0")
            return None
        # parse the first and the second part
        res1 = parse(data[1:index-1])
        if index == len(data):
            return res1
        res2 = parse(data[index + 1:])
        op = data[index]
        return resolve_op(res1, res2, op)
    # if data begins with variable, parse that variable
    index = 0
    while index < len(data) and data[index].isalpha():
        index += 1
    name = data[:index]
    # add variable to VariableNamesHolder
    idx = VariableNamesHolder().get_variable_index(name)
    if idx == -1:
        idx = VariableNamesHolder().add_variable(name)
    res1 = ZhegalkinsPolynom({BinValue([idx])})
    if index == len(data):
        return res1
    op = data[index]
    res2 = parse(data[index + 1:])
    return resolve_op(res1, res2, op)
