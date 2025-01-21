import globals

def labelhandler(linenumber, tokens):
    labelname = tokens[1]
    globals.labels[labelname] = linenumber
    
def gotohandler(tokens):
    labelname = tokens[1]
    
    if labelname in set(globals.labels.keys()):
        return globals.labels[labelname]
    else:
        raise KeyError(f"label {labelname} not found")
    
