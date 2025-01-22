import const
import globals


def parse(tokens: list | str) -> bool:
    try:
        expr = "".join(tokens)
    except:
        expr = tokens

    expr = expr.replace(const.EQUALS, "==").replace(const.GTE, ">=").replace(const.LTE, "<=")
    expr = expr.replace(const.GREATER, ">").replace(const.LESS, "<").replace(const.NOT, "!=")
    expr = expr.replace(const.LOGICAL_AND, " and ").replace(const.LOGICAL_OR, " or ").replace(const.NOT, " not ")
    expr = expr.replace(const.ADD, "+").replace(const.SUBTRACT, "minus").replace(const.MULTIPLY, "*").replace(const.DIVIDE, "/")
    
    try:
        return eval(expr, {}, globals.variables)
    except Exception as e:
        raise RuntimeError(f"error evaluating expression '{expr}': {e}")