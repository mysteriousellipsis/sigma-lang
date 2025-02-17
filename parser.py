import sys
import const
from typing import Dict, Any, List, Optional
from lexer import Lexer, Token
from const import KEYWORDS, syserr

'''
parses the list of tokens into an abstract syntax tree
each node is a dictionary to tell the evaluator how to execute the code
'''

Node = Dict[str, Any]
AST = List[Node]

class ParseError(Exception):
    '''
    for generic errors while parsing
    '''
    def __init__(self, message: Optional[str] = None) -> None:
        if message:
            super().__init__(message)
        else:
            super().__init__()

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0
        # priority for the operators for bodmas
        self.operatorpriority = {
                    "MULTIPLY": 3, "DIVIDE": 3,
                    "ADD": 2, "SUBTRACT": 2,
                    "EQUALS": 1, "GREATER": 1, "LESS": 1, "NOT": 1
                }

    def curr(self, pos: int = 0) -> Optional[Token]:
        '''
        returns the token at the current index
        '''
        return self.tokens[self.pos+pos] if self.pos+pos < len(self.tokens) else None

    def peek(self) -> Optional[Token]:
        '''returns the token at the next index'''
        return self.curr(1)

    def consume(self, expected: Optional[str] = None, errormsg: str = "", error: type = ParseError) -> Token:
        '''
        returns the token at the current index then moves on to the next index
        if the token is not of the expected type (if the expected type is given), raises an error of type error with the given error message
        '''
        token = self.curr()

        if not token:
            raise error(f"unexpected end of input {syserr}")

        if expected and token.type != expected:
            if errormsg:
                raise error(errormsg)
            raise error(f"expected {expected} but {token} is {token.type}")

        self.pos += 1

        return token

    def parse(self) -> List[Dict]:
        '''
        entry point
        '''
        ast = []

        while self.curr():
            ast.append(self.parseline())

        return ast

    def parseline(self) -> Optional[dict]:
        '''
        parses a "line"
        '''
        token = self.curr()

        if not token:
            return None

        # parses tokens based on its type
        match token.type:
            case "NEW_VAR_IDENT":
                return self.decl()
            case "IF_OPEN":
                return self.ifelse()
            case "WHILE_OPEN":
                return self.whileloop()
            case "OUTPUT":
                return self.output()
            case "INPUT":
                return self.receive()
            case "REASSIGNMENT_IDENT":
                return self.reassign()
            case "ID":
                return self.expr()
            case "COMMENT_OPEN":
                self.consume("COMMENT_OPEN")
                return None
            case "NEWLINE":
                self.consume("NEWLINE")
                return None
            case "TRY_OPEN":
                return self.tryexcept()
            case "BREAK" | "CONTINUE" | "PASS":
                return {
                    "type": "flow",
                    "name": token.type.lower()
                }
            case _:
                raise ParseError(f"unexpected token {token}{syserr}")


    def decl(self) -> Node:
        '''
        handles declaration of new variables
        '''
        self.consume("NEW_VAR_IDENT", errormsg=f"expected {KEYWORDS['NEW_VAR_IDENT']}{syserr}", error=SystemError)

        vartypetok = self.consume("TYPE", errormsg="expected a type declaration", error=SyntaxError)
        vartype = vartypetok.value

        constvar = self.consume()
        isconst = None
        # verifies if constexist is set to true
        if const.constexist:
            match constvar.type:
                case "CONST":
                    isconst = True
                case "VAR":
                    isconst = False
                case _:
                    raise SyntaxError(f"expected {KEYWORDS['CONST']} or {KEYWORDS['VAR']} after {KEYWORDS['NEW_VAR_IDENT']}")

        idtok = self.consume("ID", errormsg="expected a variable", error=SyntaxError)
        varname = idtok.value

        value = None
        if self.curr():
            if self.curr().type == "ASSIGNMENT_OPERATOR":
                self.consume("ASSIGNMENT_OPERATOR", errormsg=f"{KEYWORDS['ASSIGNMENT_OPERATOR']} expected", error=SyntaxError)
                value = self.expr()

        return {
            "type": "declaration",
            "name": varname,
            "vartype": vartype,
            "isconst": isconst if isconst else None,
            "value": value
        }

    def tryexcept(self) -> Node:
        '''
        parses try-except functions
        '''
        self.consume("TRY_OPEN", errormsg=f"expected {KEYWORDS['TRY_OPEN']}{syserr}", error=SystemError)
        self.consume("DO", errormsg=f"expected {KEYWORDS['DO']}", error=SyntaxError)

        if self.curr() == "NEWLINE":
            self.consume("NEWLINE", errormsg=f"expected a newline{syserr}", error=SystemError)

        trybody = []
        while self.curr() and self.curr().type != "EXCEPT":
            trybody.append(self.parseline())

        self.consume("EXCEPT", errormsg=f"expected {KEYWORDS['EXCEPT']}", error=SyntaxError)
        self.consume("DO", errormsg=f"expected {KEYWORDS['DO']}", error=SyntaxError)

        exceptbody = []
        while self.curr() and self.curr().type != "TRY_CLOSE":
            exceptbody.append(self.parseline())

        self.consume("TRY_CLOSE", errormsg=f"expected {KEYWORDS['TRY_CLOSE']} to end try-except", error=SyntaxError)

        return {
            "type": "try",
            "try": trybody,
            "except": exceptbody,
        }

    def ifelse(self) -> Node:
        '''parses if else'''
        self.consume("IF_OPEN", errormsg=f"expected {KEYWORDS['IF_OPEN']}{syserr}", error=SystemError)
        condition = self.evalcond()
        self.consume("THEN", errormsg=f"expected {KEYWORDS['THEN']} after {KEYWORDS['IF_OPEN']}", error=SyntaxError)
        self.consume("DO", errormsg=f"expected {KEYWORDS['DO']} after {KEYWORDS['THEN']}", error=SyntaxError)

        # gets the code that gets run in the if clause
        body = []
        while self.curr() and self.curr().type not in {"ELIF", "ELSE", "IF_CLOSE"}:
            body.append(self.parseline())

        elifs = []
        elsebody = []

        # gets the condition for the elif statement and the code that runs in the elif clause
        while self.curr() and self.curr().type == "ELIF":
            self.consume("ELIF", errormsg=f"expected {KEYWORDS['ELIF']}{syserr}", error=SystemError)
            elifcond = self.evalcond()
            self.consume("THEN", errormsg=f"expected {KEYWORDS['THEN']} after {KEYWORDS['ELIF']}", error=SyntaxError)
            self.consume("DO", errormsg=f"expected {KEYWORDS['DO']} after {KEYWORDS['THEN']}", error=SyntaxError)
            elifbody = []
            while self.curr() and self.curr().type not in {"ELIF", "ELSE", "IF_CLOSE"}:
                elifbody.append(self.parseline())

            elifs.append((elifcond, elifbody))

        # gets the code that gets run in the else clause
        if self.curr() and self.curr().type == "ELSE":
            self.consume("ELSE", errormsg=f"expected {KEYWORDS['ELSE']}{syserr}", error=SystemError)
            self.consume("DO", errormsg=f"expected {KEYWORDS['DO']} after {KEYWORDS['ELSE']}", error=SyntaxError)
            while self.curr() and self.curr().type != "IF_CLOSE":
                elsebody.append(self.parseline())

        self.consume("IF_CLOSE", errormsg=f"expected {KEYWORDS['IF_CLOSE']} to end if statement", error=SyntaxError)

        return {
            "type": "if",
            "condition": condition,
            "body": body,
            "elifs": elifs,
            "elsebody": elsebody
        }

    def whileloop(self) -> Node:
        '''handles while loops'''
        self.consume("WHILE_OPEN", errormsg=f"expected {KEYWORDS['WHILE_OPEN']}{syserr}", error=SystemError)
        condition = self.expr()
        self.consume("DO", errormsg=f"expected {KEYWORDS['DO']} after {KEYWORDS['WHILE_OPEN']}", error=SyntaxError)

        # gets the code in the while loop
        body = []
        while self.curr() and self.curr().type != "WHILE_CLOSE":
            body.append(self.parseline())

        self.consume("WHILE_CLOSE", errormsg=f"expected {KEYWORDS['WHILE_CLOSE']} to end while loop", error=SyntaxError)

        return {
            "type": "while",
            "condition": condition,
            "body": body
        }

    def output(self) -> Node:
        '''handles print statements'''
        self.consume("OUTPUT", errormsg=f"expected {KEYWORDS['OUTPUT']}{syserr}", error=SystemError)
        match self.curr().type:
            case "OUTPUT_NEWLINE":
                self.consume("OUTPUT_NEWLINE", errormsg=f"expected {KEYWORDS['OUTPUT_NEWLINE']}{syserr}", error=SystemError)
                value = self.expr()
                return {
                    "type": "output",
                    "value": value,
                    "newline": True
                }
            case _:
                value = self.expr()
                return {
                    "type": "output",
                    "value": value,
                    "newline": False
                }

    def receive(self) -> Node:
        '''handles user input'''
        self.consume("INPUT", errormsg=f"expected {KEYWORDS['INPUT']}{syserr}", error=SystemError)
        match self.curr().type:
            case "TO":
                self.consume("TO", errormsg=f"expected {KEYWORDS['TO']}{syserr}", error=SystemError)
                target = self.consume("ID", errormsg="expected a variable", error=SyntaxError).value

                return {
                    "type": "input",
                    "target": target
                }
            case _:
                return {
                    "type": "input",
                    "target": None
                }

    def reassign(self) -> Node:
        '''handles variable reassignment'''
        self.consume("REASSIGNMENT_IDENT", errormsg=f"expected {KEYWORDS['REASSIGNMENT_IDENT']}{syserr}", error=SystemError)
        varname = self.consume("ID", errormsg="expected a variable name", error=SyntaxError).value
        self.consume("TO", errormsg=f"expected {KEYWORDS['TO']} after variable name", error=SyntaxError)
        value = self.expr()

        return {
            "type": "reassignment",
            "name": varname,
            "value": value
        }

    def expr(self, priority: int = 0) -> Node:
        '''
        parses conditionals and math
        ai helped a lot with this sob
        '''
        left = self.exprhelper()
        while self.curr() and self.curr().type not in {"RIGHT_BRACKET", "NEWLINE"} and self.priority(self.curr().type) > priority:
            operator = self.consume()
            right = self.expr(self.priority(operator.type))
            left = {
                'type': 'operation',
                'op': operator.type,
                'left': left,
                'right': right
            }
        return left

    def exprhelper(self) -> Node:
        '''
        helper function for expr()
        basically just a bunch of if else statements
        '''
        token = self.consume()

        match token.type:
            case  "LEFT_BRACKET":
                expr = self.expr()
                self.consume("RIGHT_BRACKET", errormsg=f"expected {KEYWORDS['RIGHT_BRACKET']}", error=SyntaxError)
                return expr
            case _ if token.type in self.operatorpriority.keys():
                expr = self.expr()
                return expr
            case "INT" | "FLOAT":
                return {
                    "type": "literal",
                    "valtype": token.type,
                    "value": token.value
                }
            case "BOOL":
                return {
                    "type": "literal",
                    "valtype": "BOOL",
                    "value": token.value == "true"
                }
            case "STRING":
                return {
                    "type": "literal",
                    "valtype": "STRING",
                    "value": token.value
                }
            case "ID":
                return {
                    "type": "variable",
                    "name": token.value
                }
            case _:
                raise ParseError(f"invalid expression token {token.type}")

    def evalcond(self) -> Node:
        '''evaluates a condition'''
        node = self.expr()
        while self.curr() and self.curr().type not in ['RIGHT_BRACKET', 'NEWLINE', 'THEN']:
            operator = self.consume()
            right = self.expr()
            node = {
                'type': 'comparison',
                'op': operator.type,
                'left': node,
                'right': right
            }
        return node

    def priority(self, toktype: str) -> int:
        '''returns operator priority'''
        res = self.operatorpriority.get(toktype, 0)
        if not res:
            raise RuntimeError(f"{toktype} is not an operator")
        return res

# for easier debugging
if __name__ == '__main__':
    flag = sys.argv[1] if len(sys.argv) > 1 else None
    args = sys.argv[2:]

    code = None
    if flag == "--debug":
        code = "\n".join(open(file, 'r').read() for file in args)
    if code:
        print(f"code: \n{code}")

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"tokens: {tokens}\n\n")

        parser = Parser(tokens)
        ast = parser.parse()
        print(f"ast: {ast}\n\n")
