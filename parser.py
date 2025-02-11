import sys
from lexer import Lexer
from const import KEYWORDS, syserr

class ParseError(Exception):
    def __init__(self, message = ""):
        super().__init__(message)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.operatorpriority = {
                    "MULTIPLY": 3, "DIVIDE": 3,
                    "ADD": 2, "MINUS": 2,
                    "EQUALS": 1, "GREATER": 1, "LESS": 1, "NOT": 1
                }

    def curr(self, pos=0):
        '''
        returns the token at the current index
        '''
        return self.tokens[self.pos+pos] if self.pos+pos < len(self.tokens) else None

    def peek(self):
        '''
        returns the token at the next index
        '''
        return self.curr(1)

    def consume(self, expected=None):
        '''
        returns the token at the current index then moves on to the next index
        '''
        token = self.curr()

        if not token:
            raise ParseError(f"unexpected end of input {syserr}")

        if expected and token.type != expected:
            raise ParseError(f"expected {expected} but {token} is {token.type}")

        self.pos += 1

        return token

    def parse(self):
        '''main function'''
        ast = []

        while self.curr():
            ast.append(self.parseline())

        return ast

    def parseline(self):
        '''
        parses a "line"
        '''
        token = self.curr()

        if not token:
            return None

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
                self.pos += 1
                return {
                    "type": "flow",
                    "name": token.type.lower()
                }
            case _:
                raise ParseError(f"unexpected token {token} {syserr}")


    def decl(self):
        self.consume("NEW_VAR_IDENT")

        vartypetok = self.consume("TYPE")
        vartype = vartypetok.value

        constvar = self.consume()

        match constvar.type:
            case "CONST":
                isconst = True
            case "VAR":
                isconst = False
            case _:
                raise ParseError(f"expected {KEYWORDS["CONST"]} or {KEYWORDS["VAR"]} after {KEYWORDS["NEW_VAR_IDENT"]}")

        idtok = self.consume("ID")
        varname = idtok.value

        value = None
        if self.curr() and self.curr().type == "ASSIGNMENT_OPERATOR":
            self.consume("ASSIGNMENT_OPERATOR")
            value = self.expr()

        return {
            "type": "declaration",
            "name": varname,
            "vartype": vartype,
            "isconst": isconst,
            "value": value
        }

    def tryexcept(self):
        self.consume("TRY_OPEN")
        self.consume("DO")

        if self.curr() == "NEWLINE":
            self.consume("NEWLINE")

        trybody = []
        while self.curr() and self.curr().type != "EXCEPT":
            trybody.append(self.parseline())

        self.consume("EXCEPT")
        self.consume("DO")

        exceptbody = []
        while self.curr() and self.curr().type != "TRY_CLOSE":
            exceptbody.append(self.parseline())

        self.consume("TRY_CLOSE")

        return {
            "type": "try",
            "try": trybody,
            "except": exceptbody,
        }

    def ifelse(self):
        self.consume("IF_OPEN")
        condition = self.evalcond()
        self.consume("THEN")
        self.consume("DO")

        body = []
        while self.curr() and self.curr().type not in {"ELIF", "ELSE", "IF_CLOSE"}:
            body.append(self.parseline())

        elifs = []
        elsebody = []

        while self.curr() and self.curr().type == "ELIF":
            self.consume("ELIF")
            elifcond = self.evalcond()
            self.consume("THEN")
            self.consume("DO")
            elifbody = []
            while self.curr() and self.curr().type not in {"ELIF", "ELSE", "IF_CLOSE"}:
                elifbody.append(self.parseline())

            elifs.append((elifcond, elifbody))

        if self.curr() and self.curr().type == "ELSE":
            self.consume("ELSE")
            self.consume("DO")
            while self.curr() and self.curr().type != "IF_CLOSE":
                elsebody.append(self.parseline())

        self.consume("IF_CLOSE")

        return {
            "type": "if",
            "condition": condition,
            "body": body,
            "elifs": elifs,
            "elsebody": elsebody
        }

    def whileloop(self):
        self.consume("WHILE_OPEN")
        condition = self.expr()
        self.consume("DO")

        body = []

        while self.curr() and self.curr().type != "WHILE_CLOSE":
            body.append(self.parseline())

        self.consume ("WHILE_CLOSE")

        return {
            "type": "while",
            "condition": condition,
            "body": body
        }

    def output(self):
        self.consume("OUTPUT")
        match self.curr().type:
            case "OUTPUT_NEWLINE":
                self.consume("OUTPUT_NEWLINE")
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

    def receive(self):
        self.consume("INPUT")
        match self.curr().type:
            case "TO":
                self.consume("TO")
                target = self.consume("ID").value

                return {
                    "type": "input",
                    "target": target
                }
            case _:
                return {
                    "type": "input",
                    "target": None
                }

    def reassign(self):
        self.consume("REASSIGNMENT_IDENT")
        varname = self.consume("ID").value
        self.consume("TO")
        value = self.expr()

        return {
            "type": "reassignment",
            "name": varname,
            "value": value
        }

    def expr(self, priority=0):
        '''
        parses conditionals and math
        ai helped a lot with this sob
        '''
        left = self.exprhelper()
        # TODO
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

    def exprhelper(self):
        # TODO: fix this
        '''
        helper function for expr()
        basically just a bunch of if else statements
        '''
        token = self.consume()

        match token.type:
            case  "LEFT_BRACKET":
                expr = self.expr()
                self.consume("RIGHT_BRACKET")
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

    def evalcond(self):
        # TODO: fix this
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

    def priority(self, toktype):
        '''
        returns operator priority
        '''
        return self.operatorpriority.get(toktype, 0)

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
