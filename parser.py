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
            ast.append(self.parseline)
            
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
        pass

    def ifelse(self):
        pass

    def whileloop(self):
        pass

    def output(self):
        pass

    def receive(self):
        pass

    def reassign(self):
        pass

    def expr(self):
        pass