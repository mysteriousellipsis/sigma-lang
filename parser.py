from const import *

class ParseError(Exception):
    def __init__(self, message = ""):
        super().__init__(message)
        
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    def curr(self):
        '''
        returns the current token without consumitng
        '''
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self, expected=None):
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
        token = self.curr()
        if token:
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
                raise ParseError(f"unexpected token: {token[0]}")
        
    def declaration(self):
        self.consume(NEW_VAR_IDENT.upper())
        isconst = False
            
        vartype = self.consume("ID")[1]
        varname = self.consume("ID")[1]
        
        value = None

        if self.curr() and self.curr()[1] == ASSIGNMENT_OPERATOR:
            self.consume()
            value = self.expr()
            
        return ("DECLARE", varname, vartype, value, isconst)

    def ifelse(self):
        self.consume(IF_OPEN.upper())
        condition = self.expr()
        self.consume(THEN.upper())
        self.consume(DO.upper())
    
        body = []
        
        while self.curr() and self.curr()[0] not in (ELIF.upper(), ELSE.upper(), IF_CLOSE.upper()):
            body.append(self.parseline())
            
        elifs = []
        elsebod = []
        
        while self.curr() and self.curr()[0] in (ELIF.upper(), ELSE.upper()):
            if self.curr()[0] == ELIF.upper():
                self.consume()
                elifcond = self.expr()
                self.consume(THEN.upper())
                self.consume(DO.upper())
                elifbod = []
                while self.curr() and self.curr()[0] not in (ELIF.upper(), ELSE.upper(), IF_CLOSE.upper()):
                    elifbod.append(self.parseline())
                elifs.append((elifcond, elifbod))
            else:
                self.consume(ELSE.upper())
                self.consume(DO.upper())
                while self.curr() and self.curr()[0] != IF_CLOSE.upper():
                    elsebod.append(self.parseline())
        
        self.consume(IF_CLOSE.upper())
        return ("IF", condition, body, elifs, elsebod)

    def whileloop(self):
        self.consume(WHILE_OPEN.upper())
        condition = self.expr()
        self.consume(DO.upper())
        body = []
        
        while self.curr() and self.curr()[0] != WHILE_CLOSE.upper():
            body.append(self.parseline())
        
        self.consume(WHILE_CLOSE.upper())
        
        return ("WHILE", condition, body)
        
    def output(self):
        self.consume(OUTPUT.upper())
        value = self.expr()
        return ("PRINT", value)
        
    def input(self):
        self.consume(INPUT.upper())
        varname = self.consume("ID")[1]
        return ("RECEIVE", varname)
        
    def assignment(self):
        varname = self.consume("ID")[1]
        self.consume(REASSIGNMENT_OPERATOR.upper())
        value = self.expr()
        return ("ASSIGN", varname, value)
    
    def expr(self):
        token = self.consume()
        if token[0] == "INTEGER":
            return ("INTEGER", token[1])
            
        elif token[0] == "FLOAT":
            return ("FLOAT", token[1])
        
        elif token[0] == "STRING":
            return ("STRING", token[1])
            
        elif token[0] == "ID":
            return ("VARIABLE", token[1])
        
        else:
            raise ParseError(f"invalid expression {token}")