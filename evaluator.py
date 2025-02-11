import sys
from re import compile
from lexer import Lexer
from parser import Parser
from const import syserr
from globals import variables, constants

class Evaluator:
    def __init__(self):
        self.variables = variables
        self.constants = constants

    def evaluate(self, ast, mainloop=False):
        '''so that the loop isnt dead the instant theres a break or continue'''
        for node in ast:
            result = self.evalnode(node)
            if result in {"break", "continue"} and not mainloop:
                return result

    def evalnode(self, node):
        '''evaluates one node'''
        if not node:
            return

        type_ = node.get("type")

        match type_:
            case "if":
                return self.ifelse(node)
            case "try":
                return self.tryexcept(node)
            case "flow":
                return self.flowcontrol(node)
            case "input":
                return self.receive(node)
            case "while":
                return self.whileloop(node)
            case "output":
                return self.output(node)
            # case "variable":
            #     raise RuntimeError(f"")
            case "declaration":
                return self.decl(node)
            case "reassignment":
                return self.reassign(node)
            case _:
                raise RuntimeError(f"unknown node type {type_} {syserr}")

    def interpolate(self, s):
        '''helper function to evaluate interpolated strings'''
        pattern = compile(r'\$\((\w+)\)')

        def repl(match):
            varname = match.group(1)
            if varname in self.variables:
                return str(self.variables[varname][0])
            else:
                raise RuntimeError(f"undefined variable '{varname}'")

        return pattern.sub(repl, s)

    def flowcontrol(self, node):
        '''handles break, etc'''
        return node["name"]

    def tryexcept(self, node):
        '''handles try-except functions'''
        try:
            result = self.evaluate(node["try"])
            if result in {"break", "continue"}:
                return result
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            result = self.evaluate(node["except"])
            if result in {"break", "continue"}:
                return result

    def decl(self, node):
        '''handles declaration of variables'''
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
        '''handles if else statements'''
        condition = self.evalexpr(node["condition"])
        if condition:
            result = self.evaluate(node["body"])
            if result in {"break", "continue"}:
                return result

        for elifcond, elifbody in node["elifs"]:
            if self.evalexpr(elifcond):
                result = self.evaluate(elifbody)
                if result in {"break", "continue"}:
                    return result

        result = self.evaluate(node["elsebody"])
        if result in {"break", "continue"}:
            return result

    def whileloop(self, node):
        while self.evalexpr(node["condition"]):
            result = self.evaluate(node["body"])
            if result == "break":
                return
            elif result == "continue":
                continue

    def output(self, node):
        '''handles print statements'''
        value = self.evalexpr(node["value"])
        newline = node["newline"]
        if newline:
            print(value)
        else:
            print(value, end="")

    def receive(self, node):
        '''handles input'''
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
                        return float(expr["value"])
                    case "STRING":
                        return self.interpolate(expr["value"])
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
                        return left - right
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
        Evaluator().evaluate(ast, mainloop=True)
