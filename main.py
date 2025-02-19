import sys
from typing import List
from lexer import Lexer, Token
from parser import Parser, AST
from evaluator import Evaluator

"""
this is the file to run when actually using the interpreter
combines all parts of the program and checks other stuff
"""


def validatepython() -> None:
    """python version check"""
    minimum = (3, 10)
    if sys.version_info < minimum:
        print(
            f"python version {'.'.join([str(n) for n in minimum])} or higher required"
        )
        sys.exit(1)
    return None


def validatefile(filename: str) -> bool:
    try:
        if filename.endswith(".sigma"):
            return True

        with open(filename, "r") as file:
            code: str = file.read()

        firstline: List[str] = code.split("\n", 1)

        return firstline[0].strip() == "!>sigma"
    except FileNotFoundError:
        print(f"file {filename} not found")
        return False
    except Exception as e:
        print(f"error validating file: {e}")
        return False


def runfile(filename: str) -> None:
    try:
        with open(filename, "r") as file:
            code: str = file.read().strip()
        lexer: Lexer = Lexer(code)
        tokens: List[Token] = lexer.tokenize()
        parser: Parser = Parser(tokens)
        ast: AST = parser.parse()
        evaluator: Evaluator = Evaluator()
        evaluator.evaluate(ast, mainloop=True)
    except FileNotFoundError:
        print(f"error: {filename} not found")
    except KeyboardInterrupt:
        print("\nexecution interrupted by user")
        sys.exit(1)
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print("sigma intepreter")
        print("usage: sigma <file.sigma> [additional files]")
        print("       sigma <file.sigma>")
        sys.exit(0)

    for filename in sys.argv[1:]:
        if validatefile(filename):
            runfile(filename)


if __name__ == "__main__":
    main()
