import re
from const import *


OPSEQ = [
    ((EQUALS.split(), '=='),
     (GTE.split(), '>='),
     (LTE.split(), '<='),
     (GREATER.split(), '>'),
     (LESS.split(), '<'),
     (NOT.split(), '!='))
]

def tokenize(code):
    tokens = []
    # ai helped me with this im too stupi for regex
    patternmap = {
        'STRING': r'"([^"]*)"',
        'FLOAT': r'\d+\.\d+',
        'INTEGER': r'\d+',
        'OPERATOR': '|'.join(map(re.escape, [EQUALS, GTE, LTE, GREATER, LESS, NOT])),
        'SYMBOL': r'[()\[\]{};,]',
        'KEYWORD': '|'.join(map(re.escape, [ELIF, IF_OPEN, THEN, ELSE, IF_CLOSE, DO, BREAK, CONTINUE, PASS, GOTO, LABEL, WHILE_OPEN, WHILE_CLOSE, FOR_OPEN, FOR_CLOSE, IN, OUTPUT, OUTPUT_NEWLINE, INPUT, INPUT_TO])),
        'TYPE': '|'.join(map(re.escape, ALL_TYPES)),
        'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'SKIP': r'[ \t\n]+',
        'MISMATCH': r'.',
    }
    
    toxreg = '|'.join('(?P<%s>%s)' % (key, val) for key, val in patternmap.items())

    for i in re.finditer(toxreg, code):
        kind = i.lastgroup
        value = i.group()

        if kind == 'STRING':
            tokens.append(('STRING', value[1:-1]))
        elif kind == 'FLOAT':
            tokens.append(('FLOAT', float(value)))
        elif kind == 'INTEGER':
            tokens.append(('INTEGER', int(value)))
        elif kind == 'KEYWORD' or kind == 'TYPE':
            tokens.append((value.upper(), value))
        elif kind == 'OPERATOR':
            tokens.append((value, value))
        elif kind == 'SYMBOL':
            tokens.append((value, value))
        elif kind == 'ID':
            tokens.append(('ID', value))
        elif kind == 'SKIP':
            continue
        else:
            raise SyntaxError(f'unexpected character: {value}')

    i = 0
    while i < len(tokens):
        for seqwords, op in OPSEQ:
            if tokens[i:i+len(seqwords)] == [('ID', word) for word in seqwords]:
                tokens[i:i+seqwords] = [('OPERATOR', op)]
                break
        i += 1

    return tokens