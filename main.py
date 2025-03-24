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
        return self.fn(*nums)

def display_help():
    for op_obj in OPERATORS:
        print(
            'Operator: ' + op_obj.op + ' (' + op_obj.name + '); ' +
            (('Aliases: ' + ', '.join(op_obj.aliases)) if op_obj.aliases else 'No aliases')
        )

OPERATORS = [
    # Control operations
    Operator(None, 'EXIT', ['QUIT', 'ESCAPE'], lambda: None),
    Operator('?', 'HELP', ['INFO', 'OPS', 'OPERATORS'], display_help),
    
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
    Operator(None, 'ROOT', ['ROOT OPERATION'], lambda x,y: pow(x, y**-1))
]

def input_number():
    num = None

    while True:
        num = input("Input a number: ")

        try:
            num = float(num)
        except ValueError as e:
            print("Invalid number!")
            continue
        else:
            break
    
    return num

def input_operator():
    op = None

    while True:
        op_str = input("Input an operator (type 'help' for a list): ")

        for op_obj in OPERATORS:
            if op_obj.check(op_str):
                return op_obj
        
        print("No such operator found! Use 'help' to list all operators.")

num = input_number()
exit = False

while True:
    op = None

    while True:
        op = input_operator()

        if op.name == 'EXIT':
            exit = True
            break

        if op.name == 'HELP':
            op.apply()
            continue

        break

    if exit:
        break

    if op.is_unary:
        num = op.apply(num)
    else:
        num2 = input_number()

        num = op.apply(num, num2)

    print(num)
