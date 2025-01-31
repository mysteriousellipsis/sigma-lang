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
        self.consume("IF_OPEN")
        condition = self.expr()
        self.consume("THEN")
        self.consume("DO")
        
        body = []
        while self.curr() and self.curr().type not in {"ELIF", "ELSE", "IF_CLOSE"}:
            body.append(self.parseline())
            
        elifs = []
        elsebody = []
        
        while self.curr() and self.curr().type in {"ELIF", "ELSE"}:
            if self.curr().type == "ELIF":
                self.consume("ELIF")
                elifcond = self.expr()
                self.consume("THEN")
                self.consume("DO")
                elifbody = []
                while self.curr() and self.curr().type not in {"ELIF", "ELSE", "IF_CLOSE"}:
                    elifbody.append(self.parseline())
                
                elifs.append((elifcond, elifbody))
            
            if self.curr().type == "ELSE":
                self.consume("ELSE")
                self.consume("DO")
                while self.curr() and self.curr().type != "IF_CLOSE":
                    elsebody.append(self.parseline())
        
        try:
            self.consume("IF_CLOSE")
        
        except:
            print(f"{KEYWORDS['IF_CLOSE']} not found.")
            
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
        value = self.expr()
        
        return {
            "type": "output", 
            "value": value
        }

    def receive(self):
        self.consume("INPUT")
        target = self.consume("ID").value
        
        return {
            "type": "input", 
            "target": target
        }

    def reassign(self):
        self.consume("REASSIGNMENT_IDENT")
        varname = self.consume("ID").value
        self.consume("REASSIGNMENT_OPERATOR")
        value = self.expr()
        
        return {
            "type": "reassignment",
            "name": varname,
            "value": value
        }

    def expr(self):
        token = self.curr()
        
        if not token:
            raise ParseError(f"unexpected eol")
        
        if token.type == "LEFT_BRACKET":
            self.consume("LEFT_BRACKET")
            condition = self.expr()
            self.consume("RIGHT_BRACKET")
            return condition
        
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
        
        elif token.type == "ID":
            return {
                "type": "variable", 
                "name": token.value
            }
        
        else:
            raise ParseError(f"invalid expression token {token.type}")


from lexer import *

lexer = Lexer('print "some text"')

lexed = lexer.tokenize()

print(f"tokens: {lexed}")

parser = Parser(lexed)

print(f"ast: {parser.parse()}")
