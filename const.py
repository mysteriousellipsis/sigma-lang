syserr = "\nthis is most likely a problem with sigma. open an issue at https://github.com/dimini171/sigma/issues/new"
KEYWORDS = {
    "TO": "to",
    # important ntihngs
    "FILE_IDENT": "!>sigma",
    "FILE_EXT": ".sigma",

    # comments
    "COMMENT_OPEN": "<--",
    "COMMENT_CLOSE": "-->",

    # conditionals
    "ELIF": "elif",
    "IF_OPEN": "if",
    "THEN": "then",
    "ELSE": "else",
    "IF_CLOSE": "fi",
    "DO": "do",

    # assignment
    "NEW_VAR_IDENT": "let",
    "CONST": "const",
    "VAR": "var",
    "ASSIGNMENT_OPERATOR": "be",
    "REASSIGNMENT_IDENT": "change",

    # math
    "ADD": "plus",
    "SUBTRACT": "minus",
    "DIVIDE": "divided by",
    "MULTIPLY": "multiplied by",
    "MATH_OPERATORS": {"ADD", "SUBTRACT", "DIVIDE", "MULTIPLY"},

    # logic
    "EQUALS": "is equal to",
    "GTE": "is greater than or equal to",
    "LTE": "is less than or equal to",
    "GREATER": "is greater than",
    "LESS": "is less than",
    "NOT": "is not",
    "LOGICAL_AND": "and",
    "LOGICAL_OR": "or",
    "LOGICAL_OPERATORS": {"LOGICAL_AND", "LOGICAL_OR", "NOT"},

    # flow control
    "BREAK": "break",
    "CONTINUE": "continue",
    "PASS": "pass",
    "GOTO": "goto",
    "LABEL": "label",

    # i/o
    "INPUT": "receive",
    "OUTPUT": "print",
    "OUTPUT_NEWLINE": "line",

    # loops
    "WHILE_OPEN": "while",
    "WHILE_CLOSE": "elihw",
    "FOR_OPEN": "for",
    "FOR_CLOSE": "rof",
    "IN": "in",

    # vartypes
    "INTEGER": "int",
    "FLOAT": "float",
    "BOOL": "bool",
    "NONETYPE": "none",
    "STRING": "string",
    "TYPE": {"int", "float", "bool", "none", "string"},
    "BOOL_TYPES": ["true", "false"],
    "NONE_TYPES": ["none", "nothing"],


    # shell variables
    "EXIT_SHELL_STATEMENT": ["quit", "exit", "stop", "q"],
    "SHELL_PROMPT": ">> ",
}
