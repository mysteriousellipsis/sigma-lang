import const
import globals
import re


def evaluate(expr: str | list) -> any:
    '''
    evaluates the expression and parses conditionals and logic statements
    '''
    expr = " ".join(expr) if isinstance(expr, list) else expr

    expr = (
        expr.replace(const.EQUALS, "==")
        .replace(const.GTE, ">=")
        .replace(const.LTE, "<=")
        .replace(const.GREATER, ">")
        .replace(const.LESS, "<")
        .replace(const.NOT, "!=")
        .replace(const.LOGICAL_AND, " and ")
        .replace(const.LOGICAL_OR, " or ")
        .replace(const.ADD, " + ")
        .replace(const.SUBTRACT, " - ")
        .replace(const.MULTIPLY, " * ")
        .replace(const.DIVIDE, " / ")
    )

    # replaces $(variable) with the variable's value
    expr = re.sub(r"\${(\w+)}", lambda m: str(globals.variables.get(m.group(1), ['', '', ''])[2]), expr)

    varvals = {key: value[2] for key, value in globals.variables.items() if len(value) > 2}

    try:
        return eval(expr, {}, varvals)
    except NameError as e:
        raise NameError(f"You didn't define a variable!!: {e}")
    except Exception as e:
        raise RuntimeError(f"Error evaluating expression '{expr}': {e}")