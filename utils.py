import const
import globals
import re


def parse(tokens: list | str) -> bool:
    '''
    parses conditionals and logic statements
    '''
    expr = "".join(tokens) if isinstance(tokens, list) else tokens

    expr = (
        expr.replace(const.EQUALS, "==")
        .replace(const.GTE, ">=")
        .replace(const.LTE, "<=")
        .replace(const.GREATER, ">")
        .replace(const.LESS, "<")
        .replace(const.NOT, "!=")
        .replace(const.LOGICAL_AND, " and ")
        .replace(const.LOGICAL_OR, " or ")
    )

    # replaces ${variable} with the variable's value
    re.sub(r"\${(\w+)}", lambda m: str(globals.variables.get(m.group(1), ['', '', ''])[2]), expr)

    try:
        return eval(expr, {}, globals.variables)
    except Exception as e:
        raise RuntimeError(f"error evaluating expression '{expr}': {e}")


def evaluate(expr: str) -> any:
    """
    evaluates the expression using local functions
    """
    expr = (
        expr.replace(const.ADD, " + ")
        .replace(const.SUBTRACT, " - ")
        .replace(const.MULTIPLY, " * ")
        .replace(const.DIVIDE, " / ")
    )

    tokens = re.findall(r'".*?"|\S+', expr)

    for token in tokens:
        if token.startswith('"') and not token.endswith('"'):
            raise SyntaxError(f"mismatched quotes in (token)")
        
        if not token.startswith('"') and not re.match(r"\w+", token):
            raise SyntaxError(f"no quotes found in {token}")
    
    # replaces ${variable} with variable value in strings
    expr = re.sub(r"\${(\w+)}", lambda m: str(globals.variables.get(m.group(1), ['', '', ''])[2]), expr)

    try:
        return eval(expr, {}, {})
    except NameError as e:
        raise NameError(f"you didnt define a variable!!: {e}")
    except Exception as e:
        raise RuntimeError(f"error evaluating expression {expr}: {e}")
