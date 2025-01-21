import const
import globals
from typing import List


def parse(tokens: List) -> bool:
    expr = " ".join(tokens)
    expr = expr.replace(const.EQUALS, "==").replace(const.GTE, ">=").replace(const.LTE, "<=")
    expr = expr.replace(const.GREATER, ">").replace(const.LESS, "<").replace(const.NOT_EQUALS, "!=")
    expr = expr.replace(const.LOGICAL_AND, " and ").replace(const.LOGICAL_OR, " or ").replace(const.LOGICAL_NOT, " not ")
    
    try:
        return eval(expr, {}, globals.variables)
    except Exception as e:
        raise RuntimeError(f"error evaluating expression '{expr}': {e}")