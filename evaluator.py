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
            raise RuntimeError(f"unknown node type {type_} {syserr}")
        
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
        condition = self.evalexpr(node["condition"])
        if condition:
            self.evaluate(node["body"])
            return
        
        for elifcond, elifbody in node["elifs"]:
            if self.evalexpr(elifcond):
                self.evaluate(elifbody)
                return
            
        self.evaluate(node["elsebody"])
        
    def whileloop(self, node):
        while self.evalexpr(node["condition"]):
            self.evaluate(node["body"])
        
    def output(self, node):
        print(f"output {node}")
        
    def receive(self, node):
        print(f"output: {node}")
        
    def reassign(self, node):
        print(f"reassign {node}")
        
    def evalexpr(self, expr):
        if expr["type"] == "literal":
            if expr["valtype"] == "string":
                return expr["value"]
            
            try:
                if expr["valtype"] == "INT":
                    return int(expr["value"])
                
                elif expr["valtype"] == "FLOAT":
                    return float(expr["value"])
                
                else:
                    return expr["value"]
            
            except:
                return expr["value"]

        elif expr["type"] == "variable":
            if expr["name"] in self.variables:
                return self.variables[expr["name"]][0]
            raise RuntimeError(f"undefined variable {expr["name"]}")
        
        else:
            raise RuntimeError(f"unknown expression type: {expr} {syserr}")
  
from lexer import *
from parser import *
      
test = "print 'some text'"
lexer = Lexer(test)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

evaluator = Evaluator()
evaluator.evaluate(ast)