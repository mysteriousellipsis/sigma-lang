from const import *

class ParseError(Exception):
    def __init__(self, message = ""):
        super().__init__(message)
        
        
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    def curr(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self, expected=None):
        token = self.curr()
        
        if not token:
            raise ParseError("unexpected end of input\nthis is most likely a problem with sigma. open an issue at https://github.com/dimini171/sigma/issues/new")
        
        if expected and token.type != expected:
            raise ParseError(f"expected {expected} but {token} is {token.type}")
        
        self.pos += 1
        
        return token
    
    def parse(self):
        ast = []
        
        while self.curr():
            print(ast)
            ast.append(self.parseline())
            
        return ast
    
    def parseline(self):
        token = self.curr()
        
        if not token:
            return None
        
        if token.type == "NEW_VAR_IDENT":
            return self.decl()
        
        if token.type == "IF_OPEN":
            return self.ifelse()
        
        if token.type == "WHILE_OPEN":
            return self.whileloop()
        
        if token.type == "OUTPUT":
            return self.output()
        
        if token.type == "INPUT":
            return self.receive()
        
        if token.type == "REASSIGNMENT_IDENT":
            return self.reassign()
        
        if token.type == "ID":
            return self.expr()
        
        else:
            raise ParseError(f"unexpected token {token}\nthis is most likely a problem with sigma. open an issue at https://github.com/dimini171/sigma/issues/new")
        
    
    def decl(self):
        self.consume("NEW_VAR_IDENT")
        
        constvar = self.consume()
        
        if constvar.type == "CONST":
            isconst = True

        elif constvar.type == "VAR":
            isconst = False

        else:
            raise ParseError(f"expected {KEYWORDS["CONST"]} or {KEYWORDS["VAR"]} after {KEYWORDS["NEW_VAR_IDENT"]}")
        
        vartypetok = self.consume("TYPE")
        vartype = vartypetok.value
        
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
        pass

    def whileloop(self):
        pass

    def output(self):
        self.consume("OUTPUT")
        value = self.expr()
        return {"type": "input", "value": value}

    def receive(self):
        self.consume("INPUT")
        target = self.consume("ID").value
        return {"type": "input", "target": target}

    def reassign(self):
        pass

    def expr(self):
        token = self.consume()
        
        if token.type in {"INT", "FLOAT"}:
            return {"type": "literal", "type": token.type, "value": token.value}
        
        elif token.type == "BOOL":
            return {"type": "literal", "type": token.value == "true"}
        
        elif token.type == "ID":
            return {"type": "variable", "name": token.value}
        
        else:
            raise ParseError(f"invalid expression token {token.type}")

from lexer import *

lexer = Lexer("new var int variablename is 1")

lexed = lexer.tokenize()

parser = Parser(lexed)

print(f"ast: {parser.parse()}")
