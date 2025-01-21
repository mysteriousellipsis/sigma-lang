from typing import List, Any
import varhandler as var
import globals
import iohandler as io
import logichandler as cond
import flowcontrol as goto
import const
import re


def tokenize(line: str) -> List:
    """
    tokenize
    """
    return re.findall(r"\".*?\"|\S+", line)


def findblock(lines: list, startidx: int, endiden: str) -> List | int:
    """
    finds block between the start index and the
    """
    block = []

    for idx, line in enumerate(lines[startidx:], start=startidx):
        if line.strip() == endiden:
            return block, idx
        block.append(line)

    # raises error if there is no eding
    raise RuntimeError(f"expected {endiden} but could not find it :(")


def parseif(tokens, executionstack):
    '''
    experimental
    '''
    if tokens[0] == const.IF_OPEN:
        condition = " ".join(tokens[1:tokens.index(const.THEN)])
        executionstack.append(cond.parse(condition))
        return "start_if"
    
    if tokens[0] == const.ELIF:
        condition = " ".join(tokens[1:tokens.index(const.THEN)])
        if not executionstack[-1]:
            executionstack[-1] = cond.parse(condition)
        return "start_elif"
    
    if tokens[0] == const.ELSE:
        executionstack[-1] = not executionstack[-1]
        return "start_else"
    
    if tokens[0] == const.IF_CLOSE:
        executionstack.pop()
        return "end_if"
    
    return None

# def parseif(lines, startidx) -> int:
#     """
#     parses if statements and returns the index to continue at
#     """
#     conditions = []
#     blocks = []

#     idx = startidx

#     while idx < len(lines):
#         line = lines[idx].strip()

#         # if the line is an if or elif line
#         if line.startswith(const.IF_OPEN) or line.startswith(const.ELIF):
#             # finds the condition
#             condition = line.split(f"{const.THEN} {const.DO}")[0][3:].strip()
#             block, idx = findblock(lines, idx + 1, const.IF_CLOSE)
#             conditions.append(condition)
#             blocks.append(block)

#         # if the line is an else block
#         elif line == f"{const.ELSE} {const.DO}":
#             block, idx = findblock(lines, idx + 1, const.IF_CLOSE)
#             conditions.append(None)
#             blocks.append(block)

#         # if the line is the ending of the if else
#         elif line == const.IF_CLOSE:
#             break

#         # raises error if there is no if, elif, else, fi
#         else:
#             raise RuntimeError(f"Unexpected line in if block: {line}")

#     for condition, block in zip(conditions, blocks):
#         if condition is None or cond.parse(condition):
#             for line in block:
#                 # TODO:
#                 parseline(line)
#             break

#     return idx


def parsewhile(lines: List, idx: int) -> int:
    """
    parses while loops and returns the index to continue at
    """

    # finds the text starting from len(const.WHILE_OPEN)+1 (+1 is to include the space) to len(const.DO)+1
    # this means users can actually do really silly stuff lmao
    # `while                    1 == 1    do` is valid
    condition = lines[idx].strip()[len(const.WHILE_OPEN) : -len(const.DO)].strip()

    block, idx = findblock(lines, idx + 1, const.WHILE_CLOSE)

    while cond.parse(condition):
        print(f"block: {block}")
        for line in block:
            # TODO: add ability to parse nested loops and conditionals
            parseline(line)

    return idx


def parsefor(lines: List, idx: int) -> int:
    header = lines[idx].strip()
    tokens = tokenize(header)

    varname = tokens[1]

    iterable = eval(tokens[3], {}, globals.variables)

    block, idx = findblock(lines, idx + 1, const.FOR_CLOSE)

    for val in iterable:
        # stores the variable with "_forloopitered" to prevent overlapping names
        globals.variables[f"{varname}_forloopitered"] == val

        for line in block:
            parseline(line)

    return idx


def parseline(line: str, idx, executionstack) -> Any:
    # remove comments from line
    line = re.sub(f"{const.COMMENT_OPEN}.*?{const.COMMENT_CLOSE}", "", line)
    
    if not line:
        return None

    tokens = tokenize(line)
    
    if tokens[0] == const.LABEL:
        goto.labelhandler(idx, tokens)
        return None, idx+1
    
    if tokens[0] == const.REASSIGNMENT_IDENT:
        var.reassignhandler(tokens)
        return 0

    if tokens[0] == const.NEW_VAR_IDENT and tokens[1] in const.VAR_TYPES+const.CONST_TYPES:
        return var.newvarhandler(tokens), idx+1

    if tokens[0] == const.GOTO:
        return None, goto.gotohandler(tokens)
    
    if tokens[0] == const.BREAK:
        return "break", idx+1
    
    if tokens[0] == const.CONTINUE:
        return "continue", idx+1
    
    if tokens[0] == const.PASS:
        return None, idx+1
    
    if tokens[0] == const.INPUT:
        return io.recvlineshandler(tokens), idx+1

    if tokens[0] == const.OUTPUT:
        return io.printhandler(tokens), idx+1

    if tokens[0] in [const.IF_OPEN, const.ELSE, const.ELIF, const.IF_CLOSE]:
        return parseif(tokens, executionstack), idx+1

    if tokens[0] == const.WHILE_OPEN:
        # TODO:
        return const.WHILE_OPEN

    if tokens[0] == const.FOR_OPEN:
        # TODO
        return const.FOR_OPEN

    return line, idx+1
