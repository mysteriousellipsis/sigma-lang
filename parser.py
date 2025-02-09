import sys
from lexer import *
from const import *

class ParseError(Exception):
    def __init__(self, message = ""):
        super().__init__(message)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.compops = {"EQUALS", "GTE", "LTE", "GREATER", "LESS", "NOT"}
        self.operatorpriority = {
                    "MULTIPLIED_BY": 3, "DIVIDED_BY": 3,
                    "PLUS": 2, "MINUS": 2,
                    "EQUALS": 1, "GREATER": 1, "LESS": 1
                }

    def curr(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected=None):
        token = self.curr()

        if not token:
            raise ParseError(f"unexpected end of input {syserr}")

        if expected and token.type != expected:
            raise ParseError(f"expected {expected} but {token} is {token.type}")

        self.pos += 1

        return token

    def parse(self):
        ast = []

        while self.curr():
            ast.append(self.parseline())

        return ast

    def parseline(self):
        token = self.curr()

        if not token:
            return None

        if token.type == "NEW_VAR_IDENT":
            return self.decl()

        elif token.type == "IF_OPEN":
            return self.ifelse()

        elif token.type == "WHILE_OPEN":
            return self.whileloop()

        elif token.type == "OUTPUT":
            return self.output()

        elif token.type == "INPUT":
            return self.receive()

        elif token.type == "REASSIGNMENT_IDENT":
            return self.reassign()

        elif token.type == "ID":
            return self.expr()

        elif token.type == "COMMENT_OPEN":
            self.consume("COMMENT_OPEN")
            return None

        else:
            raise ParseError(f"unexpected token {token} {syserr}")


    def decl(self):
        self.consume("NEW_VAR_IDENT")

        vartypetok = self.consume("TYPE")
        vartype = vartypetok.value

        constvar = self.consume()

        if constvar.type == "CONST":
            isconst = True

        elif constvar.type == "VAR":
            isconst = False

        else:
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
            print("else detected")
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
        try:
            self.consume("OUTPUT_NEWLINE")
            value = self.expr()
            return {
                "type": "output",
                "value": value,
                "newline": True
            }
        except:
            value = self.expr()
            return {
                "type": "output",
                "value": value,
                "newline": False
            }

    def receive(self):
        self.consume("INPUT")
        try:
            self.consume("TO")
            target = self.consume("ID").value

            return {
                "type": "input",
                "target": target
            }

        except:
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

    def expr(self):
        '''
        parses conditionals and math
        '''
        left = self.exprhelper()

        # TODO

    def exprhelper(self):
        '''
        helper function for expr()
        '''
        token = self.consume()

        if token.type == "LEFT_BRACKET":
            expr = self.expr()
            self.consume("RIGHT_BRACKET")
            return expr

        token = self.consume()

        if token.type in {"INT", "FLOAT"}:
            return {
                "type": "literal",
                "valtype": token.type,
                "value": token.value
            }

        elif token.type == "BOOL":
            return {
                "type": "literal",
                "valtype": "bool",
                "value": token.value == "true"
            }

        elif token.type == "STRING":
            return {
                "type": "literal",
                "valtype": "string",
                "value": token.value
            }

        elif token.type == "ID":
            return {
                "type": "variable",
                "name": token.value
            }

        else:
            raise ParseError(f"invalid expression token {token.type}")

    def evalcond(self):
        # TODO: fix this
        node = self.expr()
        while self.curr() and self.curr().type not in ['RIGHT_BRACKET', 'NEWLINE']:
            operator = self.consume()
            right = self.expr()
            node = {
                'type': 'comparison',
                'op': operator.type,
                'left': node,
                'right': right
            }
        return node

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
            elif flag == "--default-debug":
                code = '''
new int variablename is ((5 multiplied by 4) plus (1 plus 3))
print variablename
print"variablename"
'''
            print(f"code: \n{code}")
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            print(f"tokens: {tokens}")

            parser = Parser(tokens)
            ast = parser.parse()

            print(f"ast: {ast}")
