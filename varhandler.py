import const
from exceptions import *

variables = {}

def isint(var: str) -> str:
    return var.isdigit()

def isfloat(var: str) -> str:
    try:
        float(var)
    except:
        return False
    
    if '.' in var:
        return True
    return False

def isbool(var: str) -> str:
    if var in const.BOOL_TYPES:
        return True
    return False

def isnonetype(var: str) -> str:
    if var in const.NONE_TYPES:
        return True
    return False

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

def newvarhandler(tokens):
    if len(tokens) < 6:
        raise SyntaxError("not enough arguments to make a new variable")

    if tokens[1] not in (const.CONST_TYPES + const.VAR_TYPES):
        raise SyntaxError("variable needs to be a constant or variable")
    
    if tokens[2] not in (const.INTEGER + const.BOOL + const.FLOAT + const.NONETYPE):
        raise SyntaxError("variable needs a type")
    
    if tokens[4] != const.ASSIGNMENT_OPERATOR:
        raise SyntaxError("no 'is' found :(")

    varconst = tokens[1]
    vartype = tokens[2]
    varname = tokens[3]
    varval = tokens[5:]

    if varname in set(variables.keys()):
        raise KeyError(f"this variable already exists. use `{const.REASSIGNMENT_IDENT} <variablename> {const.REASSIGNMENT_OPERATOR} <value>` to change the variable")
    
    variables[varname] = [varconst, vartype, varval]


def reassignhandler(tokens):
    if len(tokens) < 3:
        raise SyntaxError("not enough arguments")
    
    if tokens[2] != const.REASSIGNMENT_OPERATOR:
        raise SyntaxError(f"reassignment operator {const.REASSIGNMENT_OPERATOR} not found. use `{const.REASSIGNMENT_IDENT} <variablename> {const.REASSIGNMENT_OPERATOR} <value>` to change the variable")
    
    varname = tokens[1]
    varval = tokens[3]

    if varname not in set(variables.keys()):
        raise KeyError(f"variable {varname} does not exist")
    
    if variables[varname][0] in const.CONST_TYPES:
        raise ReassignmentError("unable to reassign constants")
    
    if variables[varname][1] != checktype(varval):
        raise ReassignmentError(f"variable types are not the same. cannot reassign {variables[varname][1]} to {checktype(varval)}")

    variables[varname][2] = varval