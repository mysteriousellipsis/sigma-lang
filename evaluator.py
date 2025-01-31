from const import *
from globals import *

class Evaluator:
    def __init__(self):
        self.variables = variables
        self.constants = constants

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
        varname = node["name"]
        vartype = node["vartype"]
        isconst = node["isconst"]
        value = node["value"]
        
        if varname in self.constants:
            raise RuntimeError(f"constant {varname} cannot be reassigned")
        
        if value is not None:
            evaledval = self.evalexpr(value)
            self.variables[varname] = [evaledval, vartype]
            if isconst:
                self.constants[varname] = vartype
        
    def ifelse(self, node):
        condition = self.evalcond(node["condition"])
        if condition:
            self.evaluate(node["body"])
            return
        
        for elifcond, elifbody in node["elifs"]:
            if self.evalcond(elifcond):
                self.evaluate(elifbody)
                return
            
        self.evaluate(node["elsebody"])
        
    def whileloop(self, node):
        print(f"while {node}")
        
    def output(self, node):
        print(f"output {node}")
        
    def receive(self, node):
        print(f"output: {node}")
        
    def reassign(self, node):
        print(f"reassign {node}")
        
    def evalexpr(self, expr):
        pass
    
    def evalcond(self, cond):
        pass
  
from lexer import *
from parser import *
      
test = "print 'some text'"
lexer = Lexer(test)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

evaluator = Evaluator()
evaluator.evaluate(ast)