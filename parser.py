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
        pass