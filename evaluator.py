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

        match type_:
            case "declaration":
                self.decl(node)
            case "if":
                self.ifelse(node)
            case "while":
                self.whileloop(node)
            case "output":
                self.output(node)
            case  "input":
                self.receive(node)
            case "reassignment":
                self.reassign(node)
            case _:
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
            match exptype:
                case "int":
                    self.variables[target][0] = int(usrinp)
                case "float":
                    self.variables[target][0] = float(usrinp)
                case _:
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
        match expr["type"]:
            case "literal":
                match expr["valtype"]:
                    case "INT":
                        return int(expr["value"])
                    case "FLOAT":
                        return int(expr["value"])
                    case _:
                        return expr["value"]
            case "variable":
                if expr["name"] in self.variables:
                    return self.variables[expr["name"]][0]
                raise RuntimeError(f"undefined variable {expr["name"]}")
            case "comparison" | "operation":
                left = self.evalexpr(expr["left"])
                right = self.evalexpr(expr["right"])
                op = expr["op"]

                match op:
                    case "GREATER":
                        return left > right
                    case "LESS":
                        return left < right
                    case "EQUALS":
                        return left == right
                    case "GTE":
                        return left >= right
                    case "LTE":
                        return left <= right
                    case "NOT":
                        return left != right
                    case "ADD":
                        return left + right
                    case "MULTIPLY":
                        return left * right
                    case "SUBTRACT":
                        return left * right
                    case "DIVIDE":
                        return left / right
                    case _:
                        raise RuntimeError(f"unknown comparison operator: {op}")
            case _:
                raise RuntimeError(f"unknown expression type: {expr} {syserr}")

# for easier debugging
if __name__ == '__main__':
    flag = sys.argv[1] if len(sys.argv) > 1 else None
    args = sys.argv[2:]

    code = None
    if flag == "--debug":
        code = "\n".join(open(file, 'r').read() for file in args)
    elif flag == "--default":
        code = '''
new int var iablename is ((5 multiplied by 4) plus (1 plus 3))
print iablename
print"variablename"
'''

    if code:
        print(f"code: \n{code}")

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"tokens: {tokens}\n\n")

        parser = Parser(tokens)
        ast = parser.parse()
        print(f"ast: {ast}\n\n")

        print("output:")
        Evaluator().evaluate(ast)
