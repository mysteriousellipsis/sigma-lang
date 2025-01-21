import const
import varhandler as vars

def parse(statement: str) -> bool:
    statement = statement.replace(f" {const.EQUALS} ", " == ")
    statement = statement.replace(f" {const.NOT} ", " != ")
    statement = statement.replace(f" {const.GTE} ", " >= ")
    statement = statement.replace(f" {const.LTE} ", " <= ")
    statement = statement.replace(f" {const.GREATER} ", " > ")
    statement = statement.replace(f" {const.LESS}", " < ")
    
    try:
        return eval(statement, {}, vars.variables)

    except Exception as e:
        raise RuntimeError(f"error evaluating {statement}: {e}")