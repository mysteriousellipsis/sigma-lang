import sys
import const
from typing import Dict, Any, List, Optional, Tuple
from lexer import Lexer, Token
from const import KEYWORDS, syserr

"""
parses the list of tokens into an abstract syntax tree
each node is a dictionary to tell the evaluator how to execute the code
"""

Node = Dict[str, Any]
AST = List[Node]
CondBody = List[Optional[Node]]
EOF = Token("EOF", "EOF")


class ParseError(Exception):
    """
    for generic errors while parsing
    """

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
            "MULTIPLY": 3,
            "DIVIDE": 3,
            "ADD": 2,
            "SUBTRACT": 2,
            "EQUALS": 1,
            "GREATER": 1,
            "LESS": 1,
            "NOT": 1,
        }

    def curr(self) -> Token:
        """returns the token at the current index"""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else EOF

    def peek(self) -> Token:
        """returns the token at the next index"""
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else EOF

    def consume(
        self,
        expected: Optional[str] = None,
        errormsg: Optional[str] = "",
        error: Optional[type] = ParseError,
    ) -> Token:
        """
        returns the token at the current index then moves on to the next index
        if the token is not of the expected type (if the expected type is given),
        raises an error of type error (if given) with the given error message
        """
        token = self.curr()

        if token.type == "EOF":
            raise EOFError("unexpected end of file")

        if error is not None:
            if expected and token.type != expected:
                if errormsg:
                    raise error(errormsg)
                raise error(f"expected {expected} but {token} is {token.type}")

        self.pos += 1
        return token

    def parse(self) -> AST:
        """entry point"""
        ast: AST = []

        while self.curr().type != "EOF":
            parsed: Optional[Node] = self.parseline()
            if parsed is not None:
                ast.append(parsed)

        return ast

    def parseline(self) -> Optional[Node]:
        '''parses a "line"'''
        token: Token = self.curr()

        if not token:
            return None

        # parses tokens based on its type
        match token.type:
            # code ends
            case "EOF":
                raise SystemError(f"unexpected EOF{syserr}")
            # variable declaration
            case "NEW_VAR_IDENT":
                return self.decl()
            # if statements
            case "IF_OPEN":
                return self.ifelse()
            # while loops
            case "WHILE_OPEN":
                return self.whileloop()
            # print statements
            case "OUTPUT":
                return self.output()
            # input statements
            case "INPUT":
                return self.receive()
            # variable reassignment
            case "REASSIGNMENT_IDENT":
                return self.reassign()
            # variables
            case "ID":
                return self.expr()
            # comments
            case "COMMENT_OPEN":
                self.consume("COMMENT_OPEN")
                return None
            # \n
            case "NEWLINE":
                self.consume("NEWLINE")
                return None
            # try except
            case "TRY_OPEN":
                return self.tryexcept()
            # flow control
            case "BREAK" | "CONTINUE":
                self.consume()
                return {"type": "flow", "name": token.type.lower()}
            # warnings
            case "VAR":
                raise ParseError(
                    f"unexpected token {KEYWORDS['NEW_VAR_IDENT']}\ndid you mean to declare a variable?"
                )
            case _:
                raise ParseError(f"unexpected token {token}{syserr}")

    def decl(self) -> Node:
        """
        handles declaration of new variables
        type: str
        name: str
        vartype: str
        isconst: bool
        value: Optional[Node]
        """
        self.consume(
            "NEW_VAR_IDENT",
            errormsg=f"expected {KEYWORDS['NEW_VAR_IDENT']}{syserr}",
            error=SystemError,
        )

        # tries to get variable type
        try:
            vartypetok: Token = self.consume(
                "TYPE", errormsg="expected a type declaration", error=SyntaxError
            )
        except SyntaxError as e:
            if self.peek().type in {"CONST", "VAR"}:
                raise SyntaxError(
                    f"expected a type declaration after {KEYWORDS['NEW_VAR_IDENT']}\ndid you forget to declare a type?"
                ) from e
            raise SyntaxError(
                f"expected a type declaration after {KEYWORDS['NEW_VAR_IDENT']}"
            ) from e
        vartype: str = vartypetok.value

        # tries to get variable mutability
        constvar: Token = self.consume()
        isconst: bool = False
        # verifies if constexist is set to true
        if const.constexist:
            match constvar.type:
                case "CONST":
                    isconst = True
                case "VAR":
                    isconst = False
                case _:
                    raise SyntaxError(
                        f"expected {KEYWORDS['CONST']} or {KEYWORDS['VAR']} after {KEYWORDS['NEW_VAR_IDENT']}"
                    )

        # tries to get variable name + value
        idtok: Token = self.consume(
            "ID", errormsg="expected a variable", error=SyntaxError
        )
        varname: str = idtok.value
        value: Optional[Node] = None

        if self.curr().type == "ASSIGNMENT_OPERATOR":
            self.consume(
                "ASSIGNMENT_OPERATOR",
                errormsg=f"{KEYWORDS['ASSIGNMENT_OPERATOR']} expected",
                error=SyntaxError,
            )
            value = self.expr()

        return {
            "type": "declaration",
            "name": varname,
            "vartype": vartype,
            "isconst": isconst,
            "value": value,
        }

    def tryexcept(self) -> Node:
        """
        parses try-except functions
        type: str
        try: CondBody
        except: CondBody
        """

        self.consume(
            "TRY_OPEN",
            errormsg=f"expected {KEYWORDS['TRY_OPEN']}{syserr}",
            error=SystemError,
        )
        self.consume("DO", errormsg=f"expected {KEYWORDS['DO']}", error=SyntaxError)

        # consumes the newline if it exists
        if self.curr().type == "NEWLINE":
            self.consume(
                "NEWLINE", errormsg=f"expected a newline{syserr}", error=SystemError
            )

        trybody: CondBody = []
        while self.curr().type != "EXCEPT":
            trybody.append(self.parseline())

        self.consume(
            "EXCEPT", errormsg=f"expected {KEYWORDS['EXCEPT']}", error=SyntaxError
        )
        self.consume("DO", errormsg=f"expected {KEYWORDS['DO']}", error=SyntaxError)

        exceptbody: CondBody = []
        while self.curr().type != "TRY_CLOSE":
            exceptbody.append(self.parseline())

        self.consume(
            "TRY_CLOSE",
            errormsg=f"expected {KEYWORDS['TRY_CLOSE']} to end try-except",
            error=SyntaxError,
        )

        return {
            "type": "try",
            "try": trybody,
            "except": exceptbody,
        }

    def ifelse(self) -> Node:
        """
        parses if else
        type: str
        condition: Node
        body: CondBody
        elifs: List[Tuple[Node, CondBody]]
        elsebody: CondBody
        """
        self.consume(
            "IF_OPEN",
            errormsg=f"expected {KEYWORDS['IF_OPEN']}{syserr}",
            error=SystemError,
        )
        condition: Node = self.evalcond()
        self.consume(
            "THEN",
            errormsg=f"expected {KEYWORDS['THEN']} after {KEYWORDS['IF_OPEN']}",
            error=SyntaxError,
        )
        self.consume(
            "DO",
            errormsg=f"expected {KEYWORDS['DO']} after {KEYWORDS['THEN']}",
            error=SyntaxError,
        )

        # gets the code that gets run in the if clause
        body: CondBody = []
        while self.curr().type not in {"ELIF", "ELSE", "IF_CLOSE"}:
            body.append(self.parseline())

        elifs: List[Tuple[Node, CondBody]] = []
        elsebody: CondBody = []

        # gets the condition for the elif statement and the code that runs in the elif clause
        while self.curr().type == "ELIF":
            self.consume(
                "ELIF",
                errormsg=f"expected {KEYWORDS['ELIF']}{syserr}",
                error=SystemError,
            )
            elifcond: Node = self.evalcond()
            self.consume(
                "THEN",
                errormsg=f"expected {KEYWORDS['THEN']} after {KEYWORDS['ELIF']}",
                error=SyntaxError,
            )
            self.consume(
                "DO",
                errormsg=f"expected {KEYWORDS['DO']} after {KEYWORDS['THEN']}",
                error=SyntaxError,
            )
            elifbody: CondBody = []
            while self.curr().type not in {"ELIF", "ELSE", "IF_CLOSE"}:
                elifbody.append(self.parseline())

            elifs.append((elifcond, elifbody))

        # gets the code that gets run in the else clause
        if self.curr().type == "ELSE":
            self.consume(
                "ELSE",
                errormsg=f"expected {KEYWORDS['ELSE']}{syserr}",
                error=SystemError,
            )
            self.consume(
                "DO",
                errormsg=f"expected {KEYWORDS['DO']} after {KEYWORDS['ELSE']}",
                error=SyntaxError,
            )
            while self.curr().type != "IF_CLOSE":
                elsebody.append(self.parseline())

        self.consume(
            "IF_CLOSE",
            errormsg=f"expected {KEYWORDS['IF_CLOSE']} to end if statement",
            error=SyntaxError,
        )

        return {
            "type": "if",
            "condition": condition,
            "body": body,
            "elifs": elifs,
            "elsebody": elsebody,
        }

    def whileloop(self) -> Node:
        """
        handles while loops
        type: str
        condition: Node
        body: CondBody
        """
        self.consume(
            "WHILE_OPEN",
            errormsg=f"expected {KEYWORDS['WHILE_OPEN']}{syserr}",
            error=SystemError,
        )
        condition: Node = self.expr()
        self.consume(
            "DO",
            errormsg=f"expected {KEYWORDS['DO']} after {KEYWORDS['WHILE_OPEN']}",
            error=SyntaxError,
        )

        # gets the code in the while loop
        body: CondBody = []
        while self.curr().type != "WHILE_CLOSE":
            body.append(self.parseline())

        self.consume(
            "WHILE_CLOSE",
            errormsg=f"expected {KEYWORDS['WHILE_CLOSE']} to end while loop",
            error=SyntaxError,
        )

        return {"type": "while", "condition": condition, "body": body}

    def output(self) -> Node:
        """
        handles print statements
        type: str
        value: Optional[Node]
        newline: bool
        """
        self.consume(
            "OUTPUT",
            errormsg=f"expected {KEYWORDS['OUTPUT']}{syserr}",
            error=SystemError,
        )
        newline: bool = False
        value: Optional[Node] = None
        match self.curr().type:
            case "OUTPUT_NEWLINE":
                self.consume(
                    "OUTPUT_NEWLINE",
                    errormsg=f"expected {KEYWORDS['OUTPUT_NEWLINE']}{syserr}",
                    error=SystemError,
                )
                value = self.expr()
                newline = True
            case _:
                value = self.expr()

        return {"type": "output", "value": value, "newline": newline}

    def receive(self) -> Node:
        """
        handles user input
        type: str
        target: Optional[str]
        """
        self.consume(
            "INPUT", errormsg=f"expected {KEYWORDS['INPUT']}{syserr}", error=SystemError
        )
        target: Optional[str] = None
        if self.curr().type == "TO":
            self.consume(
                "TO", errormsg=f"expected {KEYWORDS['TO']}{syserr}", error=SystemError
            )
            target = self.consume(
                "ID", errormsg="expected a variable", error=SyntaxError
            ).value

        return {"type": "input", "target": target}

    def reassign(self) -> Node:
        """
        handles variable reassignment
        type: str
        name: str
        value: Node
        """
        self.consume(
            "REASSIGNMENT_IDENT",
            errormsg=f"expected {KEYWORDS['REASSIGNMENT_IDENT']}{syserr}",
            error=SystemError,
        )
        varname: str = self.consume(
            "ID", errormsg="expected a variable name", error=SyntaxError
        ).value
        self.consume(
            "TO",
            errormsg=f"expected {KEYWORDS['TO']} after variable name",
            error=SyntaxError,
        )
        value: Node = self.expr()

        return {"type": "reassignment", "name": varname, "value": value}

    def expr(self, priority: int = 0) -> Node:
        """
        parses conditionals and math
        ai helped a lot with this sob
        type: str
        op: str
        left: Node
        right: Node
        """
        left: Node = self.exprhelper()
        while (
            self.curr().type not in {"RIGHT_BRACKET", "NEWLINE", "DO", "THEN"}
            and self.priority(self.curr().type) > priority
        ):
            operator: str = self.consume().type
            right: Node = self.expr(self.priority(operator))
            left = {"type": "operation", "op": operator, "left": left, "right": right}
        return left

    def exprhelper(self) -> Node:
        """
        helper function for expr()
        basically just a bunch of if else statements
        type: str
        valtype: Optional[str]
        value: Optional[str]
        name: Optional[str]
        """
        token = self.consume()

        match token.type:
            case "LEFT_BRACKET":
                expr = self.expr()
                self.consume(
                    "RIGHT_BRACKET",
                    errormsg=f"expected {KEYWORDS['CLOSE_PAREN']}",
                    error=SyntaxError,
                )
                return expr
            case _ if token.type in self.operatorpriority.keys():
                expr = self.expr()
                return expr
            case "INT" | "FLOAT":
                return {"type": "literal", "valtype": token.type, "value": token.value}
            case "BOOL":
                return {
                    "type": "literal",
                    "valtype": "BOOL",
                    "value": token.value == "true",
                }
            case "STRING":
                return {"type": "literal", "valtype": "STRING", "value": token.value}
            case "ID":
                return {"type": "variable", "name": token.value}
            case _:
                raise ParseError(f"invalid expression token {token.type}")

    def evalcond(self) -> Node:
        """
        evaluates a condition
        type: str
        op: str
        left: Node
        right: Node
        """
        node: Node = self.expr()
        while self.curr().type not in ["RIGHT_BRACKET", "NEWLINE", "THEN"]:
            operator: str = self.consume().type
            right: Node = self.expr()
            node = {"type": "comparison", "op": operator, "left": node, "right": right}
        return node

    def priority(self, toktype: str) -> int:
        """returns operator priority"""
        res = self.operatorpriority.get(toktype, 0)
        if not res:
            raise RuntimeError(f"{toktype} is not an operator")
        return res


# for easier debugging
if __name__ == "__main__":
    flag = sys.argv[1] if len(sys.argv) > 1 else None
    args = sys.argv[2:]

    code = None
    if flag == "--debug":
        code = "\n".join(open(file, "r").read() for file in args)
    if code:
        print(f"code: \n{code}")

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"tokens: {tokens}\n\n")

        parser = Parser(tokens)
        ast = parser.parse()
        print(f"ast: {ast}\n\n")
