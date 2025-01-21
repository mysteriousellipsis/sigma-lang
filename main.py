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
    
    if filename[-6:0] != ".sigma":
        if not lines:
            return 0

        if lines[0] != const.FILE_IDENT:
            raise RuntimeError("file does not have identifier !>sigma")
        else:
            raise RuntimeError("wrong file extension... rename your files to <filename>.sl then try again!")
    
    # parse the files
    for line in lines:
        if parser.parseline(line):
            # TODO: handle if else and loops
            pass

if len(args) == 0:
    # shell mode soon?
    raise RuntimeError("no file was provided :(")

else:
    for filename in args:
        mainloop(filename)
