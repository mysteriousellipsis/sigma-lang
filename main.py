import sys
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

def validatepython():
    '''python version check'''
    minimum = (3, 10)
    if sys.version_info < minimum:
        print(f"python version {'.'.join([str(n) for n in minimum])} or high required")
        sys.exit()

def validatefile(filename):
    try:
        if filename.endswith('.sigma'):
            return True

        with open(filename, 'r') as file:
            code = file.read()

        firstline = code.split('\n', 1)

        return firstline[0].strip() == '!>sigma'
    except FileNotFoundError:
        print(f"file {filename} not found")
        return False
    except Exception as e:
        print(f"error validating file: {e}")
        return False

def runfile(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read().strip()
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        evaluator.evaluate(ast)
    except FileNotFoundError:
        print(f"error: {filename} not found")
    except KeyboardInterrupt:
        print("\nexecution interrupted by user")
        sys.exit(1)

def main():
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
