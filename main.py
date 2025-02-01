import sys
from lexer import *
from parser import *
from evaluator import *
from globals import *

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
        
def main():
    if len(sys.argv) < 2:
        print("sigma intepreter")
        print("usage: sigma <file.sigma> [additional files]")
        print("       sigma <file.sigma>")
        print()
        sys.exit()
        
    for filename in sys.argv[1:]:
        if not validatefile(filename):
            continue
        
        try:
            runfile(filename)
        
        except KeyboardInterrupt:
            print(f"\n Execution interrupted by user")
            sys.exit()
            
if __name__ == "__main__":
    main()