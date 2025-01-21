from typing import List, Any
import varhandlers as var
import const
import re


def tokenize(statement: str) -> List:
    return statement.split()


def printlinehandler(tokens):
    # print line
    if tokens[1] == const.OUTPUT_NEWLINE:
        print(f"{tokens[2:]}")

    # print
    else:
        print(f"{tokens[1:]}")
        

def recvlineshandler(tokens) -> str:
    # input to variable
    if (
        len(tokens) == 3
        and tokens[1] == const.INPUT_TO
        and tokens[3] in set(vars.variables.keys())
    ):
        
        usrinput = input()
        vars.variables[tokens[3]] = usrinput

    return usrinput



def parseline(line: str) -> Any:
    # remove comments from line
    line = re.sub(f"{const.COMMENT_OPEN}.*?{const.COMMENT_CLOSE}", "", line)

    if not line:
        return None

    tokens = tokenize(line)

    if tokens[0] == const.REASSIGNMENT_IDENT:
        return var.reassignhandler(tokens)

    if tokens[0] == const.NEW_VAR_IDENT:
        return var.newvarhandler(tokens)

    if tokens[0] == const.INPUT:
        return recvlineshandler(tokens)
    
    if tokens[0] == const.OUTPUT:
        return printlinehandler(tokens)
    
    

    return
