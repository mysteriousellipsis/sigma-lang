import const
import globals
import re


def printhandler(tokens: list) -> None:
    if len(tokens) <= 1:
        print()

    # print line
    elif tokens[1] == const.OUTPUT_NEWLINE:
        printline(tokens)

    # print
    else:
        printnoline(tokens)


def removequotes(text: str):
    '''
    removes quotes from 
    '''
    return text.strip('"')


def printnoline(tokens: list) -> None:
    # TODO:
    tokens = [removequotes(token) for token in tokens]
    if tokens[1] in globals.variables:
        print(f"{globals.variables[tokens[1]][2]}{' '.join(tokens[2:])}", end="")
    else:
        print(' '.join([re.sub(r"\${(\w+)}", 
                               lambda m: str(globals.variables.get(m.group(1), ['', '', ''])[2]), 
                               token) for token in tokens[1:]]), end="")


def printline(tokens: list) -> None:
    tokens = [removequotes(token) for token in tokens]

    if tokens[2] in globals.variables:
        print(f"{globals.variables[tokens[2]][2]}{' '.join(tokens[3:])}")
    else:
        print(f"{' '.join([re.sub(r"\${(\w+)}", 
                                  lambda m: str(globals.variables.get(m.group(1), ['', '', ''])[2]), 
                                  token) for token in tokens[2:]])}")


def recvlineshandler(tokens: list) -> str:
    # input to variable
    if len(tokens) == 3 and tokens[1] == const.INPUT_TO:
        usrinput = input()
        globals.variables[tokens[2]] = [const.VAR_TYPES[0], const.STRING, usrinput]
        return usrinput

    return ""
