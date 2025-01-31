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
        
keywords = []

for phrase in keywordsinv.keys():
    keywords.append(phrase)
    
keywords.sort(key=lambda x: len(x), reverse=True)
escapedkw = [re.escape(kw) for kw in keywords]
kwpattern = '|'.join(escapedkw)\

pattern = fr'''
            ("[^"]*"|'[^']*')|
            ({kwpattern})|
            ([()])|
            (\d+\.\d+|\.\d+|\d+)|
            (\w+)|
            ([^\s\w])
        '''

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
        self.words = re.findall(pattern, text, re.VERBOSE)
        self.words = [next(group for group in match if group) for match in self.words]
        self.currword = self.words[self.pos] if self.pos < len(self.words) else None

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
            
            if word.startswith('"') and word.endswith('"') or word.startswith("'") and word.endswith("'"):
                tokens.append(Token('STRING', word[1:-1]))
                self.next()
                continue
            
            if word == '(':
                tokens.append(Token('LEFT_BRACKET'))
                self.next()
                continue
                
            if word == ')':
                tokens.append(Token('RIGHT_BRACKET'))
                self.next()
                continue
                
            if word in keywordsinv:
                tokens.append(Token(keywordsinv[word]))
                self.next()
                continue
            
            elif word in KEYWORDS['BOOL_TYPES']:
                tokens.append(Token('BOOL', word))
            
            elif word in KEYWORDS['NONE_TYPES']:
                tokens.append(Token('NONETYPE', word))
                
            elif word.isdigit():
                tokens.append(Token('INT', word))
                
            elif self.isfloat(word):
                tokens.append(Token("FLOAT", word))
            
            else:
                tokens.append(Token("ID", word))
                
            self.next()
            
        return tokens