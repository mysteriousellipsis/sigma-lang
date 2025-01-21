import const
import sys
import shell
import parser
import varhandler as vars

args = sys.argv[1:]

def mainloop(filename: str) -> int | str:
    with open(filename, "r") as file:
        # reads all lines that have content AND removes blank lines
        lines = [line.strip() for line in file if line.strip()]
    
    # raises error if file format is wrong
    if not filename.endswith(".sigma"):
        if not lines:
            return 0
        
        if lines[0] != const.FILE_IDENT and filename[-6:0] != ".sigma":
            raise RuntimeError("file does not have identifier !>sigma")
        raise RuntimeError("wrong file extension... rename your files to <filename>.sl then try again!")
    
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        
        # runs parseline
        result = parser.parseline(line)

        # if there is an if block
        if result == const.IF_OPEN:
            idx = parser.parseif(lines, idx)

        elif result == const.WHILE_OPEN:
            idx = parser.parsewhile(lines, idx)

        elif result == const.FOR_OPEN:
            idx = parser.parsefor(lines, idx)

        idx += 1


if len(args) == 0:
    # shell mode soon?
    raise RuntimeError("no file was provided :(")

else:
    for filename in args:
        mainloop(filename)
