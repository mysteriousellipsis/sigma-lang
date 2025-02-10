import sys
from lexer import *
from parser import *
from const import *
from globals import *

# TODO

class Evaluator:
    def __init__(self):
        self.variables = variables
        self.constants = constants

    def evaluate(self, ast):
        for node in ast:
            self.evalnode(node)

    def evalnode(self, node):
        if not node:
            return

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
        value = self.evalexpr(node["value"])
        newline = node["newline"]
        if newline:
            print(value)
        else:
            print(value, end="")

    def receive(self, node):
        target = node["target"]
        if not target:
            input()
            return None

        if target not in self.variables:
            raise RuntimeError(f"undefined variable {target}")

        usrinp = input()

        exptype = self.variables[target][1]

        try:
            if exptype == "int":
                self.variables[target][0] = int(usrinp)
            elif exptype == "float":
                self.variables[target][0] = float(usrinp)
            else:
                self.variables[target][0] = usrinp

        except ValueError:
            raise RuntimeError(f"input should be {exptype} but wrong type was provided")

    def reassign(self, node):
        varname = node['name']

        if varname in self.constants:
            raise RuntimeError(f"constant {varname} cannot be changed")

        if varname not in self.variables:
            raise RuntimeError(f"undefined variable: {varname}")

        value = self.evalexpr(node["value"])
        self.variables[varname][0] = value

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
        elif expr["type"] == "comparison":
            left = self.evalexpr(expr["left"])
            right = self.evalexpr(expr["right"])
            op = expr["op"]

            if op == "GREATER":
                return left > right
            elif op == "LESS":
                return left < right
            elif op == "EQUALS":
                return left == right
            elif op == "GTE":
                return left >= right
            elif op == "LTE":
                return left <= right
            elif op == "NOT":
                return left != right
            else:
                raise RuntimeError(f"Unknown comparison operator: {op}")
        elif expr["type"] == "operation":
            # TODO: math
            op = expr["op"]
            left = self.evalexpr(expr["left"])
            right = self.evalexpr(expr["right"])

            match op:
                case "ADD":
                    return left+right
                case "MULTIPLY":
                    return left*right
                case "SUBTRACT":
                    return left*right
                case "DIVIDE":
                    return left/right
                case _:
                    raise RuntimeError(f"unknown operator: {op}")
        else:
            raise RuntimeError(f"unknown expression type: {expr} {syserr}")

# for easier debugging
if __name__ == '__main__':
    flag = None
    if len(sys.argv) > 1:
        try:
            flag = sys.argv[1]
        except:
            pass

        args = sys.argv[2:]
        if flag:
            code = None
            if flag == "--debug":
                for file in args:
                    code = open(file, 'r').read()
            elif flag == "--default":
                code = '''
new int var iablename is ((5 multiplied by 4) plus (1 plus 3))
print iablename
print"variablename"
'''
            print(f"code: \n{code}")
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            print(f"tokens: {tokens}")

            parser = Parser(tokens)
            ast = parser.parse()

            print(f"ast: {ast}")

            evaluator = Evaluator()
            evaluator.evaluate(ast)
