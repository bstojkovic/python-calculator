import math

class Operator:
    def __init__(self, op, name, aliases, fn, is_unary=False):
        self.op = op
        self.name = name

        if self.op is None:
            self.op = self.name

        self.aliases = aliases
        self.fn = fn
        self.is_unary = is_unary

    def check(self, op):
        op = op.upper()

        if self.op == op:
            return True

        if self.name == op:
            return True

        if op in self.aliases:
            return True

        return False

    def apply(self, *nums):
        try:
            return self.fn(*nums)
        except ValueError as e:
            print("Invalid number for operation!")
            print(e)
        except ZeroDivisionError as e:
            print("Division by zero is not allowed!")
            print(e)

        return None

def display_help():
    for op_obj in OPERATORS:
        print(
            'Operator: ' + op_obj.op + ' (' + op_obj.name + '); ' +
            (('Aliases: ' + ', '.join(op_obj.aliases)) if op_obj.aliases else 'No aliases')
        )

OPERATORS = [
    # Control operations
    Operator(None, 'EXIT', ['QUIT', 'ESCAPE'], lambda: None),
    Operator('?', 'HELP', ['LIST', 'INFO', 'OPS', 'OPERATORS'], display_help),
    Operator(None, 'CLEAR', ['CLR'], lambda: None),
    Operator(None, 'MEM', ['MEMORY', 'MEMORIZE'], lambda: None, True),

    # Basic arithmetic
    Operator('+', 'PLUS', ['ADD', 'ADDITION'], lambda x,y: x+y),
    Operator('-', 'MINUS', ['SUB', 'SUBTRACT', 'SUBTRACTION'], lambda x,y: x-y),
    Operator('*', 'TIMES', ['MUL', 'MULT', 'MULTIPLY', 'MULTIPLICATION'], lambda x,y: x*y),
    Operator('/', 'OVER', ['DIV', 'DIVIDE', 'DIVIDE BY'], lambda x,y: x/y),
    Operator('^', 'POWER', ['POW', 'TO THE POWER OF'], lambda x,y: x**y),

    # Basic unary operators
    Operator(None, 'NEG', ['NEGATIVE', 'NEGATE'], lambda x: -x, True),
    Operator(None, 'SQRT', ['SQUARE ROOT'], lambda x: math.sqrt(x), True),
    Operator(None, 'LOG10', ['LOG 10', 'LOG_10'], lambda x: math.log10(x), True),
    Operator(None, 'LOG2', ['LOG 2', 'LOG_2'], lambda x: math.log2(x), True),
    Operator(None, 'LN', ['LOG NATURAL', 'NATURAL LOG'], lambda x: math.log(x, math.e), True),

    # Other binary operators
    Operator(None, 'ROOT', ['ROOT OPERATION'], lambda x,y: pow(x, y**-1)),
    Operator(None, 'LOG', ['GENERAL LOG'], lambda x,y: math.log(x, y))
]

class SpecialNumber:
    def __init__(self, name, value):
        self.name = name
        self.value = value

SPECIAL_NUMBERS = [
    SpecialNumber('e', math.e),
    SpecialNumber('pi', math.pi),
    SpecialNumber('mem', '<mem>')
]

MEMORY = {
    'num': None,
    'mem_num': None
}

def catch_special_number(num):
    for num_obj in SPECIAL_NUMBERS:
        if num_obj.name == num:
            return num_obj.value

    return None

def input_number():
    num = input("Input a number: ")
    invalid_num = False

    try:
        num = float(num)
    except ValueError as e:
        spec_num = catch_special_number(num)

        if spec_num is None:
            invalid_num = True
        elif spec_num == '<mem>':
            return MEMORY['mem_num']
        else:
            return spec_num

    if invalid_num:
        print("Invalid number!")
        return input_number()

    return num

def input_operator():
    op_str = input("Input an operator (type 'help' for a list): ")

    for op_obj in OPERATORS:
        if op_obj.check(op_str):
            return op_obj

    print("No such operator found! Use 'help' to list all operators.")

    return input_operator()

def apply_unary_operator(op, num):
    temp_num = op.apply(num)

    if temp_num is not None:
        num = temp_num

    return num

def apply_binary_operator(op, num, num2):
    temp_num = op.apply(num, num2)

    if temp_num is not None:
        num = temp_num

    return num

def main():
    global MEMORY
    num = MEMORY['num']

    # Gather input

    if num is None:
        num = input_number()

    op = input_operator()

    # Handle special operators

    if op.name == 'EXIT':
        return -1

    if op.name == 'HELP':
        op.apply()
        return 0

    if op.name == 'CLEAR':
        num = input_number()
        MEMORY['num'] = None
        return 0

    if op.name == 'MEM':
        MEMORY['mem_num'] = num
        MEMORY['num'] = None
        return 0
    
    # Apply the operator

    if op.is_unary:
        num = apply_unary_operator(op, num)
    else:
        num2 = input_number()
        num = apply_binary_operator(op, num, num2)
    
    # Store and print the result

    MEMORY['num'] = num
    print(num)

while True:
    status_code = main()

    if status_code == -1:
        break
