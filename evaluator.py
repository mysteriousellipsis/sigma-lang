import sys
from re import compile, Pattern, Match
from typing import Optional, Dict, Any, Union
from lexer import Lexer
from parser import Parser, AST, Node
from const import syserr
import globals

EvalType = Union[int, float, str, bool, None]


class Evaluator:
    def __init__(self) -> None:
        self.variables: Dict[str, Any] = globals.variables
        self.constants: Dict[str, Any] = globals.constants

    def evaluate(self, ast: AST, mainloop: bool = False) -> Optional[str]:
        """so that the loop isnt dead the instant theres a break or continue"""
        for node in ast:
            result: Optional[str] = self.evalnode(node)
            if result in {"break", "continue"} and not mainloop:
                return result
        return None

    def evalnode(self, node: Node) -> Optional[str]:
        """evaluates one node"""
        if not node:
            return None

        type_: str = node["type"]

        match type_:
            case "if":
                return self.ifelse(node)
            case "try":
                return self.tryexcept(node)
            case "flow":
                return self.flowcontrol(node)
            case "input":
                self.receive(node)
            case "while":
                return self.whileloop(node)
            case "output":
                self.output(node)
            case "declaration":
                return self.decl(node)
            case "reassignment":
                self.reassign(node)
            case "variable":
                return type_
            case _:
                raise RuntimeError(f"unknown node type {type_} {syserr}")
        return None

    def interpolate(self, s: str) -> str:
        """helper function to evaluate interpolated strings"""
        pattern: Pattern[str] = compile(r"\$\((\w+)\)")

        def repl(match: Match[str]) -> str:
            varname = match.group(1)
            if varname in self.variables:
                return str(self.variables[varname][0])
            else:
                raise RuntimeError(f"undefined variable '{varname}'")

        return pattern.sub(repl, s)

    def flowcontrol(self, node: Node) -> str:
        """handles break, etc"""
        res: str = node["name"]
        return res

    def tryexcept(self, node: Node) -> Optional[str]:
        """handles try-except functions"""
        result: Optional[str] = None
        try:
            result = self.evaluate(node["try"])
            if result in {"break", "continue"}:
                return result
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            # print(e)
            result = self.evaluate(node["except"])
            if result in {"break", "continue"}:
                return result
        return None

    def decl(self, node: Node) -> Optional[str]:
        """handles declaration of variables"""
        varname: str = node["name"]
        vartype: str = node["vartype"]
        isconst: bool = node["isconst"]
        value: Node = node["value"]

        if varname in self.constants:
            raise RuntimeError(f"constant {varname} cannot be reassigned")

        if value is not None:
            evaledval = self.evalexpr(value)
            self.variables[varname] = [evaledval, vartype]
            if isconst:
                self.constants[varname] = vartype
        return None

    def ifelse(self, node: Node) -> Optional[str]:
        """handles if else statements"""
        condition = self.evalexpr(node["condition"])
        result: Optional[str] = None
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
        return None

    def whileloop(self, node: Node) -> Optional[str]:
        result: Optional[str] = None
        while self.evalexpr(node["condition"]):
            result = self.evaluate(node["body"])
            if result == "break":
                return None
            elif result == "continue":
                continue
        return result

    def output(self, node: Node) -> None:
        """handles print statements"""
        value: EvalType = self.evalexpr(node["value"])
        newline: bool = node["newline"]
        if newline:
            print(value)
        else:
            print(value, end="")
        return None

    def receive(self, node: Node) -> None:
        """handles input"""
        target: Optional[str] = node["target"]
        if not target:
            input()
            return None

        if target not in self.variables:
            raise RuntimeError(f"undefined variable {target}")

        usrinp: str = input()

        exptype: str = self.variables[target][1]

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
        return None

    def reassign(self, node: Node) -> None:
        varname: str = node["name"]

        if varname in self.constants:
            raise RuntimeError(f"constant {varname} cannot be changed")

        if varname not in self.variables:
            raise RuntimeError(f"undefined variable: {varname}")

        value: Optional[EvalType] = self.evalexpr(node["value"])
        self.variables[varname][0] = value
        return None

    def evalexpr(self, expr: Node) -> EvalType:
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
                        val: EvalType = expr["value"]
                        return val
            case "variable":
                if expr["name"] in self.variables:
                    varval: EvalType = self.variables[expr["name"]][0]
                    return varval
                raise RuntimeError(f"undefined variable {expr['name']}")
            case "comparison" | "operation":
                left = self.evalexpr(expr["left"])
                right = self.evalexpr(expr["right"])
                op = expr["op"]
                if left is None or right is None:
                    raise RuntimeError("cannot compare None")
                elif isinstance(left, str) or isinstance(right, str):
                    if op == "EQUALS":
                        return left == right
                    raise RuntimeError("cannot compare strings")
                elif isinstance(left, bool) and isinstance(right, bool):
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
                elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
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
if __name__ == "__main__":
    flag = sys.argv[1] if len(sys.argv) > 1 else None
    args = sys.argv[2:]

    code = None
    if flag == "--debug":
        code = "\n".join(open(file, "r").read() for file in args)
    elif flag == "--default":
        code = """
new int var iablename is ((5 multiplied by 4) plus (1 plus 3))
print iablename
print"variablename"
"""

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
