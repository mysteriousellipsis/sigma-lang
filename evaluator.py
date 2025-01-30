from const import *
from globals import *

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, ast):
        for node in ast:
            self.evalnode(node)

    def evalnode(self, node):
        '''
        parses the nodes n stuff
        '''
        if node[0] == "DECLARE":
            self.decl(node)

        elif node[0] == "IF":
            self.ifelse(node)
        
        elif node[0] == "WHILE":
            self.whileloop(node)

        elif node[0] == "PRINT":
            self.output(node)

        elif node[0] == "RECEIVE":
            self.receive(node)

        elif node[0] == "ASSIGN":
            self.assign(node)

        else:
            raise RuntimeError(f"unknown node type: {node[0]}\n this is most likely a problem with sigmalang. please open an issue at https://github.com/dimini171/sigma/issues")
        
    def evalcond(self, condition):
        '''
        evaluates conditions
        '''
        # TODO: make this actually work???
        return eval(condition)
    
    def decl(self, node):
        _, varname, vartype, value, isconst = node
        
        # TODO: add type checking

        if varname in self.constants:
            raise RuntimeError(f"constant {varname} cannot be changed")
        
        if value is not None:
            variables[varname] = [value, vartype]
            
            if isconst:
                constants.add(varname)
    
    def ifelse(self, node):
        _, condition, body, elifs, elsebod = node

        if self.evalcond(condition):
            self.evaluate(body)
            return
        
        for elifcond, elifbod in elifs:
            if self.evalcond(elifcond):
                self.evaluate(elifbod)
                return
            
        self.evaluate(elsebod)
    
    def whileloop(self, node):
        _, condition, body = node

        while self.evalcond(condition):
            self.evaluate(body)
            
    def output(self, node):
        _, value = node

        print(value)
        
    def receive(self, node):
        _, varname = node
        usrinp = input()
        try:
            variables[varname][0] = [usrinp]
        except:
            print(f"variable {varname} does not exist")
            
    def assign(self, node):
        _, name, value = node

        if name in constants:
            raise RuntimeError(f"constant {name} cannot be changed")
        
        try:
            variables[name][0] = value
        except:
            print(f"variable {name} does not exist. ")
            
    def evalexpr(self, expr):
        if expr[0] == "INTEGER":
            return int(expr[1])
        
        elif expr[0] == "FLOAT":
            return float(expr[1])
        
        elif expr[0] == "STRING":
            return str(expr[1])
        
        elif expr[0] == "VARIABLE":
            if expr[1] not in variables:
                raise RuntimeError(f"variable {expr[1]} is undefined")
            
            return variables[expr[1]]

        else:
            raise RuntimeError(f"unknown expression type: {expr[0]}\n this is most likely a problem with sigmalang. please open an issue at https://github.com/dimini171/sigma/issues")