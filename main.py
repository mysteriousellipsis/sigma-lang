import const
import sys
import parser


def mainloop(filename: str) -> int | str:
    with open(filename, "r") as file:
        # reads all lines that have content AND removes blank lines
        lines = [line.strip() for line in file if line.strip()]

    # raises error if file format is wrong
    if not filename.endswith(const.FILE_EXT):
        if not lines:
            return 0

        if lines[0] != const.FILE_IDENT and filename[-6:0] != const.FILE_EXT:
            raise RuntimeError(f"file does not have identifier {const.FILE_IDENT}")
        raise RuntimeError(
            f"wrong file extension... rename your files to <filename>{const.FILE_EXT} then try again!"
        )

    executionstack = []
    idx = 0

    while idx < len(lines):
        line = lines[idx]
        result, idx = parser.parseline(lines, line, idx, executionstack)

        if result is not None and (not executionstack or executionstack[-1]):
            if result == "break":
                break
            elif result == "continue":
                continue
            else:
                print(f"{result}")


args = sys.argv[1:]

if len(args) == 0:
    # shell mode soon?
    raise RuntimeError("no file was provided :(")

else:
    for filename in args:
        mainloop(filename)
