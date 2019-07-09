def typeLetter(t): return t[0]

def scalarType(t):
    scalarTypes = {
        "int": "float",
        "float": "float",
        "double": "double"
    }
    return scalarTypes[t]

def unique(lst):
    used = []
    res = []
    for e in lst:
        if e not in used:
            used.append(e)
            res.append(e)
    return res

