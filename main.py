import sys
from lexer import *
from parser import *
from evaluator import *

def validatefile(filename):
    if filename.endswith('.sigma'):
        return True
    
    with open(filename, 'r') as file:
        code = file.read()
        
    
    firstline = code.split('\n', 1)
    
    return firstline[0].strip() == '!>sigma'

def main(filename):
    with open(filename, 'r') as file:
        code = file.read()
        
    # tokens = tokenize(code)
    # parser = Parser(tokens)
    # ast = parser.parse()
    # evaluator = Evaluator()
    # evaluator.evaluate(ast)

args = sys.argv

if len(args) < 2:
    # if user runs `sigma`
    # potential shell?
    print("run sigma <filename>.sigma to run a script")
    sys.exit()

for filename in args[1:]:
    validatefile(filename)
    main(filename)