class ParseError(Exception):
    def __init__(self, message = ""):
        super().__init__(message)
        
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        
    def curr(self):
        return self.tokens[self.pos] if self.pon < len(self.tokens) else None