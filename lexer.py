import re
from const import *

keywordsinv = {}
for k,v in KEYWORDS.items():
    if isinstance(v, list):
        for item in v:
            keywordsinv[item] = k
    elif isinstance(v, set):
        continue
    else:
        keywordsinv[v] = k

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.words = re.findall(r'("[^"]*"|\'[^\']*\')|([()])|(\w+)|([^\s\w])', text, re.VERBOSE)
        self.words = [next(group for group in match if group) for match in self.words]
        self.currword = self.words[self.pos] if self.pos < len(self.words) else None
        print(f"words: {self.words}")

    def next(self):
        self.pos += 1
        if self.pos < len(self.words):
            self.currword = self.words[self.pos]
        else:
            self.currword = None
            
    def isfloat(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def tokenize(self):
        tokens = []
        
        while self.currword is not None:
            word = self.currword
            
            print(f"word: {word}")
            
            if word == '(':
                tokens.append(Token('LEFT_BRACKET'))
                
            elif word == ')':
                tokens.append(Token('RIGHT_BRACKET'))
            
            elif word.startswith('"') and word.endswith('"') or word.startswith("'") and word.endswith("'"):
                tokens.append(Token('ID', word[1:-1]))
            
            elif word in KEYWORDS['BOOL_TYPES']:
                tokens.append(Token('BOOL', word))
            
            elif word in KEYWORDS['NONE_TYPES']:
                tokens.append(Token('NONETYPE', word))
                
            elif word.isdigit():
                tokens.append(Token('INT', word))
                
            elif self.isfloat(word):
                tokens.append(Token("FLOAT", word))
                
            elif word in keywordsinv:
                type__ = keywordsinv[word]
                
                if word in {v for k in KEYWORDS['TYPE'] for v in [KEYWORDS[k]]}:
                    tokens.append(Token('TYPE', word))
            
                else:
                    tokens.append(Token(type__))
            
            else:
                tokens.append(Token("ID", word))
                
            self.next()
            
        return tokens
    

# lexer = Lexer("new var int variablename is 1")
# print(lexer.tokenize())
# outputs `[NEW_VAR_IDENT, VAR, :int, ID:variablename, ASSIGNMENT_OPERATOR, INT:1]`