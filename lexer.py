import re
import sys
from const import KEYWORDS

keywordsinv = {}
for key, value in KEYWORDS.items():
    if isinstance(value, list):
        for item in value:
            keywordsinv[item] = key
    elif isinstance(value, set):
        continue
    else:
        keywordsinv[value] = key

keywords = []

for phrase in keywordsinv.keys():
    keywords.append(phrase)

keywords = sorted(keywordsinv.keys(), key=len, reverse=True)
escapedkw = [re.escape(kw) for kw in keywords]
kwpattern = r'\b(?:' + '|'.join(escapedkw) + r')\b' # changed this so that it matches keywords and ids properly

pattern = re.compile(fr'''
            (<--[\s\S]*?-->)|     # comments
            ("[^"]*"|'[^']*')|    # strings (stuff between "" and '')
            ({kwpattern})|        # stuff from const.py
            ([()])|               # parenthesis
            (\d+\.\d+|\.\d+|\d+)| # ints and floats
            (\w+)|                # identifiers
            (\n)|                 # newlines
            ([^\s\w])             # characters
        ''',
        re.VERBOSE | re.DOTALL
)

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

        # finds all matches
        # extracts the first non-empty group from each match (tuple)
        self.words = [
            next(group for group in match if group)
            for match in pattern.findall(text)
        ]

        self.currword = self.words[self.pos] if self.pos < len(self.words) else None

    def next(self):
        self.pos += 1
        if self.pos < len(self.words):
            self.currword = self.words[self.pos]
        else:
            self.currword = None

    @staticmethod
    def isfloat(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def tokenize(self):
        tokens = []

        for word in self.words:
            if word == '\n':
                tokens.append(Token('NEWLINE'))
                continue
            elif word.startswith('<--') and word.endswith('-->'):
                continue
            elif (word.startswith('"') and word.endswith('"')) or (word.startswith("'") and word.endswith("'")):
                tokens.append(Token('STRING', word[1:-1]))
                continue
            elif word == '(':
                tokens.append(Token('LEFT_BRACKET'))
                continue
            elif word == ')':
                tokens.append(Token('RIGHT_BRACKET'))
                continue
            elif word in KEYWORDS["TYPE"]:
                tokens.append(Token("TYPE", word))
                continue
            elif word in KEYWORDS['BOOL_TYPES']:
                tokens.append(Token('BOOL', word))
            elif word in KEYWORDS['NONE_TYPES']:
                tokens.append(Token('NONETYPE', word))
            elif word.isdigit():
                tokens.append(Token('INT', word))
            elif self.isfloat(word):
                tokens.append(Token("FLOAT", word))
            elif word in keywordsinv:
                tokens.append(Token(keywordsinv[word]))
                continue
            else:
                tokens.append(Token("ID", word))
        return tokens

# for easier debugging
if __name__ == '__main__':
    flag = sys.argv[1] if len(sys.argv) > 1 else None
    args = sys.argv[2:]

    code = None
    if flag == "--debug":
        code = "\n".join(open(file, 'r').read() for file in args)
    elif flag == "--default":
        code = '''
new int var iablename is ((5 multiplied by 4) plus (1 plus 3))
print iablename
print"variablename"
'''

    if code:
        print(f"code: \n{code}")

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"tokens: {tokens}\n\n")
