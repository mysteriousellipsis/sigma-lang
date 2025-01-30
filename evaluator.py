from const import *
from globals import *

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, ast):
        for node in ast:
            self.evalnode(node)

    def evalnode(self, node):
        if node[0] == "DECLARE":
            pass

        elif node[0] == "IF":
            pass
        
        elif node[0] == "WHILE":
            pass

        elif node[0] == "PRINT":
            pass

        elif node[0] == "RECEIVE":
            pass

        elif node[0] == "ASSIGN":
            pass

        else:
            raise RuntimeError(f"unknown node type: {node[0]}")
    
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

        pass
    