from const import *

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
        if not token:
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
        if token[0] == NEW_VAR_IDENT.upper():
            return self.declaration()
        
        elif token[0] == IF_OPEN.upper():
            return self.ifelse()
        
        elif token[0] == WHILE_OPEN.upper():
            return self.whileloop()
        
        elif token[0] == OUTPUT.upper():
            return self.output()
        
        elif token[0] == INPUT.upper():
            return self.input()
        
        elif token[0] == 'ID':
            return self.assignment()
        
        else:
            raise(ParseError(f"unexpected token: {token[0]}"))
        
    def declaration(self):
        self.consume(NEW_VAR_IDENT.upper())
        isconst = False

        if self.curr()[1] in CONST_TYPES:
            self.consume()
            isconst = True

        elif self.curr()[1] in VAR_TYPES:
            self.consume()
        
        else:
            raise ParseError("expected variable or constant type")
            
        vartype = self.consume("ID")[1]
        varname = self.consume("ID")[1]
        
        value = None

        if self.curr() and self.curr()[1] == ASSIGNMENT_OPERATOR:
            self.consume()
            value = self.expr()
            
        return ("DECLARE", varname, vartype, value, isconst)

    def ifelse(self):
        pass

    def whileloop(self):
        pass
        
    def output(self):
        pass
        
    def input(self):
        pass
        
    def assignment(self):
        pass
    
    def expr(self):
        pass