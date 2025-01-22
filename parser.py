from typing import List, Any
import varhandler as var
import globals
import iohandler as io
import utils as logic
import flowcontrol as goto
import const
import re


def tokenize(line: str) -> List:
    """
    tokenizes line
    """
    return re.findall(r'".*?"|\S+', line)


def findblock(lines: list, idx: int, endiden: str):
    """
    finds block between the start index and the
    """
    block = []

    for i in range(idx, len(lines)):
        line = lines[i].strip()
        if line == endiden:
            return block, i
        block.append(line)
    raise SyntaxError(f"expected {endiden} but could not find it")


def parseif(tokens, executionstack):
    """
    experimental
    """
    if tokens[0] == const.IF_OPEN:
        condition = " ".join(tokens[1 : tokens.index(const.THEN)])
        executionstack.append(logic.evaluate(condition))
        return "start_if"

    if tokens[0] == const.ELIF:
        condition = " ".join(tokens[1 : tokens.index(const.THEN)])
        if not executionstack[-1]:
            executionstack[-1] = logic.evaluate(condition)
        return "start_elif"

    if tokens[0] == const.ELSE:
        executionstack[-1] = not executionstack[-1]
        return "start_else"

    if tokens[0] == const.IF_CLOSE:
        executionstack.pop()
        return "end_if"


def parsewhile(lines: List, idx: int) -> int:
    """
    parses while loops and returns the index to continue at
    """

    # finds the text starting from len(const.WHILE_OPEN)+1 (+1 is to include the space) to len(const.DO)+1
    # this means users can actually do really silly stuff lmao
    # `while                    1 == 1    do` is valid
    condition = lines[idx][len(const.WHILE_OPEN): -len(const.DO)].strip()

    block, idx = findblock(lines, idx + 1, const.WHILE_CLOSE)

    while logic.evaluate(condition):
        for line in block:
            result, _ = parseline(lines, line, idx, [])
            if result == "break":
                return idx
            elif result == "continue":
                break

    return idx + 1


def parsefor(lines: List, idx: int) -> int:
    header = lines[idx].strip()
    tokens = tokenize(header)

    varname = tokens[1]

    iterable = eval(tokens[3], {}, globals.variables)

    block, idx = findblock(lines, idx + 1, const.FOR_CLOSE)

    for val in iterable:
        # stores the variable with "_forloopitered" to prevent overlapping names
        globals.variables[f"{varname}_forloopitered"] = [
            const.VAR_TYPES[0],
            const.STRING,
            val,
        ]

        for line in block:
            parseline(lines, line, idx, [])

    return idx


def parseline(lines, line: str, idx, executionstack) -> Any:
    # remove comments from line
    line = re.sub(f"{const.COMMENT_OPEN}.*?{const.COMMENT_CLOSE}", "", line)

    if not line:
        return None, idx + 1

    tokens = tokenize(line)

    if tokens[0] == const.LABEL:
        goto.labelhandler(idx, tokens)
        return None, idx + 1

    if tokens[0] == const.REASSIGNMENT_IDENT:
        return var.reassignhandler(tokens), idx + 1

    if (
        tokens[0] == const.NEW_VAR_IDENT
        and tokens[1] in const.VAR_TYPES + const.CONST_TYPES
    ):
        return var.newvarhandler(tokens), idx + 1

    if tokens[0] == const.GOTO:
        return None, goto.gotohandler(tokens)

    if tokens[0] == const.BREAK:
        return "break", idx + 1

    if tokens[0] == const.CONTINUE:
        return "continue", idx + 1

    if tokens[0] == const.PASS:
        return None, idx + 1

    if tokens[0] == const.INPUT:
        return io.recvlineshandler(tokens), idx + 1

    if tokens[0] == const.OUTPUT:
        return io.printhandler(tokens), idx + 1

    if tokens[0] in [const.IF_OPEN, const.ELSE, const.ELIF, const.IF_CLOSE]:
        parseif(tokens, executionstack)
        return None, idx + 1
    
    if tokens[0] == const.FILE_IDENT:
        return None, idx + 1
    
    if tokens[0] == const.WHILE_OPEN:
        return None, parsewhile(lines, idx)
    
    if tokens[0] == const.WHILE_CLOSE:
        return None, idx + 1

    raise KeyError(f"unrecognized argument {tokens[0]}")
