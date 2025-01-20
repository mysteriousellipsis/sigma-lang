import const
import sys
import shell
import vars

args = sys.argv[1:]

if len(args) == 0:
    # shell mode soon?
    raise RuntimeError("no file was provided :(")


else:
    for filename in args:
        with open(filename, "r") as file:
            # reads all lines that have content AND removes blank lines
            lines = [line.strip() for line in file if line.strip()]
        
        if filename[-3:0] != ".sl" and lines[0] != const.FILE_IDENT:
            raise RuntimeError("wrong file extension... rename your files to <filename>.sl then try again!")
        
        # parse the files
        