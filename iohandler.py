import const

def printlinehandler(tokens):
    # print line
    if tokens[1] == const.OUTPUT_NEWLINE:
        print(f"{''.join(tokens[2:])}")

    # print
    else:
        print(f"{''.join(tokens[1:])}")
        

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

