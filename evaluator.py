from const import *
from globals import *

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, ast):
        for node in ast:
            self.evalnode(node)
  
  
from lexer import *
from parser import *
      
test = "print 'some text'"
lexer = Lexer(test)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

evaluator = Evaluator()
evaluator.evaluate(ast)