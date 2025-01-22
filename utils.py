import const
import globals


def parse(tokens: list | str) -> bool:
    try:
        expr = "".join(tokens)
    except:
        expr = tokens

    expr = (
        expr.replace(const.EQUALS, "==")
        .replace(const.GTE, ">=")
        .replace(const.LTE, "<=")
    )
    expr = (
        expr.replace(const.GREATER, ">")
        .replace(const.LESS, "<")
        .replace(const.NOT, "!=")
    )
    expr = (
        expr.replace(const.LOGICAL_AND, " and ")
        .replace(const.LOGICAL_OR, " or ")
        .replace(const.NOT, " not ")
    )
    expr = (
        expr.replace(const.ADD, "+")
        .replace(const.SUBTRACT, "minus")
        .replace(const.MULTIPLY, "*")
        .replace(const.DIVIDE, "/")
    )

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

    expr.strip("'").strip('"')

    # tokens = re.findall(r"\".*?\"|\S+", expr)
    tokens = expr.split()

    for i, token in enumerate(tokens):
        if (
            token.strip() in globals.variables
        ):  # replace variable names with their values
            tokens[i] = f"{ str(globals.variables[token][2])} "

    expr = " ".join(tokens)

    try:
        return eval(expr, {}, {})
    except NameError as e:
        raise NameError(f"you didnt define a variable!!: {e}")
    except Exception as e:
        raise RuntimeError(f"error evaluating expression {expr}: {e}")
