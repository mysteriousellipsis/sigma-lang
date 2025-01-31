from const import *
from globals import *

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, ast):
        for node in ast:
            self.evalnode(node)
            
    def evalnode(self, node):
        type_ = node.get("type")
        
        if type_ == "declaration":
            self.decl(node)
            
        elif type_ == "if":
            self.ifelse(node)
            
        elif type_ == "while":
            self.whileloop(node)
            
        elif type_ == "output":
            self.output(node)
            
        elif type_ == "input":
            self.receive(node)
            
        elif type_ == "reassignment":
            self.reassign(node)
        
        else:
            raise RuntimeError(f"unknown node type {type_}\nthis is most likely a problem with sigmalang. open an issue at https://github.com/dimini171/sigma/issues/new")
        
    def decl(self, node):
        print(f"declaration {node}")
        
    def ifelse(self, node):
        print(f"if {node}")
        
    def whileloop(self, node):
        print(f"while {node}")
        
    def output(self, node):
        print(f"output {node}")
        
    def receive(self, node):
        print(f"output: {node}")
        
    def reassign(self, node):
        print(f"reassign {node}")
  
from lexer import *
from parser import *
      
test = "print 'some text'"
lexer = Lexer(test)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

evaluator = Evaluator()
evaluator.evaluate(ast)