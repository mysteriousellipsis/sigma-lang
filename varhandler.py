import const
import globals
from exceptions import *


def isint(var: str) -> str:
    return var.isdigit()


def isfloat(var: str) -> str:
    try:
        float(var)
    except:
        return False

    return "." in var


def isbool(var: str) -> str:
    return var in const.BOOL_TYPES


def isnonetype(var: str) -> str:
    return var in const.NONE_TYPES


def checktype(var: str) -> str:
    if isint(var):
        return const.INTEGER

    elif isfloat(var):
        return const.FLOAT

    elif isbool(var):
        return const.BOOL

    elif isnonetype(var):
        return const.NONETYPE

    return const.STRING


def evaluate(expr: str) -> bool:
    try:
        return eval(expr, {}, globals.variables)
    except Exception as e:
        raise RuntimeError(f"error evaluating expression {expr}: {e}")


def newvarhandler(tokens: list) -> str:
    if len(tokens) < 6:
        raise SyntaxError("not enough arguments to make a new variable")

    if tokens[1] not in (const.CONST_TYPES + const.VAR_TYPES):
        raise SyntaxError("variable needs to be a constant or variable")

    if tokens[2] not in const.ALL_TYPES:
        raise SyntaxError("variable needs a type")

    if tokens[4] != const.ASSIGNMENT_OPERATOR:
        raise SyntaxError("no 'is' found :(")

    varconst = tokens[1]
    vartype = tokens[2]
    varname = tokens[3]
    
    if varname in set(globals.variables.keys()):
        raise KeyError(
            f"{varname} already exists. use `{const.REASSIGNMENT_IDENT} <variablename> {const.REASSIGNMENT_OPERATOR} <value>` to change the variable"
        )
    
    if len(tokens) > 5 and tokens[4] == const.ASSIGNMENT_OPERATOR:
        value = evaluate(" ".join(tokens[5:]))
        globals.variables[varname] = [varconst, vartype, value]
        return f"assigned {value} to {varname}"
    
    globals.variables[varname] = [varconst, vartype, None]
    return f"declared {varname} without value"


def reassignhandler(tokens: list) -> None:
    if len(tokens) < 3:
        raise SyntaxError("not enough arguments")

    if tokens[2] != const.REASSIGNMENT_OPERATOR:
        raise SyntaxError(
            f"reassignment operator {const.REASSIGNMENT_OPERATOR} not found. use `{const.REASSIGNMENT_IDENT} <variablename> {const.REASSIGNMENT_OPERATOR} <value>` to change the variable"
        )

    varname = tokens[1]
    varval = tokens[3]

    if varname not in globals.variables:
        raise KeyError(f"variable {varname} does not exist")

    if globals.variables[varname][0] in const.CONST_TYPES:
        raise ReassignmentError("unable to reassign constants")

    if globals.variables[varname][1] != checktype(varval):
        raise ReassignmentError(
            f"variable types are not the same. cannot reassign {globals.variables[varname][1]} to {checktype(varval)}"
        )

    globals.variables[varname][2] = varval
