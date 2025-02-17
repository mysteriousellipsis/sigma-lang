import re
import sys
import const
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Pattern, cast

'''
lexer for the language
tokenizes the input into tokens (duh) that the parser can understand.
this part of the program removes noise like whitespace and comments
'''

# this chunk of code is a little confusing
#
# keywordsinv: inverted version of const.KEYWORDS
# keywordsonly: list of keys of const.KEYWORDS, sorted by length in descending order
# escapedkw and kwpattern: regex related variables, dont touch unless you know what you're doing

keywordsinv: Dict[str, str] = {}
for key, value in const.KEYWORDS.items():
    if key in const.NOLOOKUP:
        continue
    if isinstance(value, dict):
        # for nested dictionaries (e.g. MATH_OPERATORS, LOGICAL_OPERATORS)
        for inner_key, inner_val in value.items():
            keywordsinv[inner_val] = inner_key
    elif isinstance(value, str):
        keywordsinv[value] = key

keywordsonly: List[str] = sorted(list(keywordsinv.keys()), key=len, reverse=True)
escapedkw: List[str] = [re.escape(kw) for kw in keywordsonly]
kwpattern: str = r'\b(?:' + '|'.join(escapedkw) + r')\b' # changed this so that it matches keywords and ids only if they are not part of a larger word

pattern: Pattern[str] = re.compile(fr'''
            ({re.escape(str(const.KEYWORDS["COMMENT_OPEN"]))}[\s\S]*?{re.escape(str(const.KEYWORDS["COMMENT_CLOSE"]))}) |     # comments
            ("[^"]*"|'[^']*') |    # strings (stuff between "" and '')
            ({kwpattern}) |        # stuff from const.py
            ([()]) |               # parenthesis
            (\d+\.\d+|\.\d+|\d+) | # ints and floats
            (\w+) |                # identifiers
            (\n) |                 # newlines
            ([^\s\w])              # characters
        ''',
        re.VERBOSE | re.DOTALL
)

@dataclass()
class Token:
    '''
    token data type
    '''
    def __init__(self, type_: str, value: str="") -> None:
        self.type: str = type_
        self.value: str = value

    def __repr__(self) -> str:
        '''defines what the token looks like when printed'''
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

    def __eq__(self, other: Any) -> bool:
        '''defines how to compare tokens'''
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value

class Lexer:
    '''lexer'''
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.pos: int = 0

        # precompute regex pattern
        self.words: List[str] = [
            next(group for group in match if group)
            for match in pattern.findall(text)
        ]

        self.currword: Optional[str] = self.words[self.pos] if self.pos < len(self.words) else None

    def next(self) -> None:
        self.pos += 1
        self.currword = self.words[self.pos] if self.pos < len(self.words) else None

    @staticmethod
    def isfloat(x: str) -> bool:
        '''
        returns if argument `x` is a float without modifying the value
        '''
        try:
            s = x
            float(s)
            return True
        except ValueError:
            return False

    def tokenize(self) -> list[Token]:
        '''
        entry point
        '''
        tokens: List[Token] = []

        for word in self.words:
            # newline
            if word == '\n':
                tokens.append(Token('NEWLINE'))
                continue
            # comments
            elif word[0] == const.KEYWORDS['COMMENT_OPEN'] and word[-1] == const.KEYWORDS['COMMENT_CLOSE']:
                continue
            # strings
            elif (word[0] in const.KEYWORDS['STRING_DELIMS'] and
                  word[-1] in const.KEYWORDS['STRING_DELIMS'] and
                  word[0] == word[-1]):
                tokens.append(Token('STRING', word[1:-1]))
                continue
            # brackets
            elif word == const.KEYWORDS['OPEN_PAREN']:
                tokens.append(Token('LEFT_BRACKET'))
                continue
            elif word == const.KEYWORDS['CLOSE_PAREN']:
                tokens.append(Token('RIGHT_BRACKET'))
                continue
            # types (int, float, str, none)
            elif word in cast(Dict[str, str], const.KEYWORDS["TYPE"]).values():
                tokens.append(Token("TYPE", word))
                continue
            # booltypes (true, false)
            elif word in const.KEYWORDS['BOOL_TYPES']:
                tokens.append(Token('BOOL', word))
            # nonetypes
            elif word in const.KEYWORDS['NONE_TYPES']:
                tokens.append(Token('NONETYPE', word))
            # integers
            elif word.isdigit():
                tokens.append(Token('INT', word))
            # floats
            elif self.isfloat(word):
                tokens.append(Token("FLOAT", word))
            # other keywords
            elif word in keywordsinv:
                tokens.append(Token(keywordsinv[word]))
                continue
            # identifiers (can contain errornous stuff but thats handled by the parser)
            else:
                tokens.append(Token("ID", word))
        return tokens

# for easier debugging
# run python lexer.py --debug <file> to see the tokens
if __name__ == '__main__':
    flag = sys.argv[1] if len(sys.argv) > 1 else None
    args = sys.argv[2:]

    code = None
    if flag == "--debug":
        code = "\n".join(open(file, 'r').read() for file in args)

    if code:
        print(f"code: \n{code}")

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"tokens: {tokens}\n\n")
