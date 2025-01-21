from typing import List, Any
import varhandler as var
import iohandler as io
import const
import re


def tokenize(statement: str) -> List:
    return statement.split()


def parseline(line: str) -> Any:
    # remove comments from line
    line = re.sub(f"{const.COMMENT_OPEN}.*?{const.COMMENT_CLOSE}", "", line)

    if not line:
        return None

    tokens = tokenize(line)

    if tokens[0] == const.REASSIGNMENT_IDENT:
        var.reassignhandler(tokens)
        return 0

    if tokens[0] == const.NEW_VAR_IDENT:
        var.newvarhandler(tokens)
        return 0

    if tokens[0] == const.INPUT:
        io.recvlineshandler(tokens)
        return 0
    
    if tokens[0] == const.OUTPUT:
        io.printlinehandler(tokens)
        return 0
    
    
    if tokens[0] == const.IF_OPEN:
        return const.IF_OPEN

    if tokens[0] == const.WHILE_OPEN:
        return const.WHILE_OPEN

    if tokens[0] == const.FOR_OPEN:
        return const.FOR_OPEN
    

    return
