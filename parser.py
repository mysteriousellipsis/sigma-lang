class ParseError(Exception):
    def __init__(self, message = ""):
        super().__init__(message)
        
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        
    def curr(self):
        '''
        returns the current token without consumitng
        '''
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self, expected=None:
        token = self.curr()
        if token is None:
            raise ParseError("unexpected eol")
            
        if expected and token[0] != expected:
            raise ParseError(f"expected {expected} but got {token[0]} instead")
            
        self.pos += 1
        return token
    
    def parse(self):
        ast = []
        while self.curr():
            ast.append(self.parseline())
        return ast

    def parseline(self):
        # TODO
        token = self.curr()
        if token[0] == 'NEW':
            pass
        
        elif token[0] == 'IF':
            pass
        
        elif token[0] == 'WHILE':
            pass
        
        elif token[0] == 'PRINT':
            pass
        
        elif token[0] == 'RECEIVE':
            pass
        
        elif token[0] == 'ID':
            pass
        
        else:
            raise(ParseError(f"unexpected token: {token[0]}"))
        
    def declaration(self):
        pass

    def ifelse(self):
        pass

    def 