from typing import Set, Dict, Union

# system settings
syserr = "\nthis is most likely a problem with sigma. open an issue at https://github.com/dimini171/sigma/issues/new"
NOLOOKUP: Set[str] = {"TYPE", "BOOL_TYPES", "NONE_TYPES", "STRING_OPEN", "STRING_CLOSE"}
constexist: bool = True

KEYWORDS: Dict[str, Union[str, Dict[str, str], Set[str]]] = {
    "TO": "to",
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
    "MATH_OPERATORS": {
            "ADD": "plus",
            "SUBTRACT": "minus",
            "DIVIDE": "divided by",
            "MULTIPLY": "multiplied by"
        },

    # logic
    "EQUALS": "equals",
    "GTE": "is more than or equal to",
    "LTE": "is less than or equal to",
    "GREATER": "is more than",
    "LESS": "is less than",
    "LOGICAL_OPERATORS": {
            "LOGICAL_AND": "and",
            "LOGICAL_OR": "or",
            "NOT": "is not"
        },

    # flow control
    "BREAK": "break",
    "CONTINUE": "continue",
    # "PASS": "pass",
    # to be added
    # "GOTO": "goto",
    # "LABEL": "label",

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
    "TYPE": {
        "INTEGER": "int",
        "FLOAT": "float",
        "BOOL": "bool",
        "NONETYPE": "none",
        "STRING": "string"
    },
    "BOOL_TYPES": {"true", "false"},
    "NONE_TYPES": {"none", "nothing"},

    # try-except
    "TRY_OPEN": "try",
    "EXCEPT": "except",
    "TRY_CLOSE": "yrt",

    # shell variables (shell mode to be added)
    # "EXIT_SHELL_STATEMENT": ["quit", "exit", "stop", "q"],
    # "SHELL_PROMPT": ">> ",
    #
    # standard sybols, dont change
    "STRING_DELIMS": {"'", '"'},
    "OPEN_PAREN": "(",
    "CLOSE_PAREN": ")",
}
