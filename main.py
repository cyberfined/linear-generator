#!/usr/bin/python
import vector
import matrix
import funcType
from utils import unique

def sortByType(vecs):
    groups = []
    indices = dict()
    maxIndex = 0
    for v in vecs:
        if v.getScalar() not in indices:
            indices[v.getScalar()] = maxIndex
            groups.append([v])
            maxIndex+=1
        else:
            groups[indices[v.getScalar()]].append(v)
    return groups

def genCFile(vecs, hfile):
    res = """\
#include "{0}"
#include <stddef.h>
#include <math.h>\n\n"""
    res = res.format(hfile)
    generics = []
    particulars = []
    for grp in sortByType(vecs):
        funcs = []
        defs = []
        for g in grp: 
            pfs = g.getParticularFuncs()
            if pfs:
                d = [f.getBody(g.getType(), g.getScalar(), g.getSize()) for f in pfs]
                defs.append("\n\n".join(d))
            funcs.extend(g.getGenericFuncs())
        particulars.append("\n\n".join(defs))
        generics.append("\n\n".join([f.getBody(grp[0].getScalar()) for f in unique(funcs)]))

    generics = "\n\n".join(generics)
    particulars = "\n\n".join(particulars)
    res += "\n\n".join([generics, particulars])
    return res

def genHFile(vecs):
    types = []
    protos = []
    res = "#pragma once\n\n"
    for v in vecs:
        types.append(v.getDefinition())

        pfs = v.getParticularFuncs()
        if pfs:
            protos.append("\n".join([f.getProto(v.getType(), v.getScalar()) for f in pfs]))
    
    types = "\n".join(types)
    protos = "\n\n".join(protos)
    res += "\n\n".join([types, protos])
    return res

def genLinearLib(libname, vecs):
    hfile = libname + ".h"
    cfile = libname + ".c"

    hcont = genHFile(vecs)
    ccont = genCFile(vecs, hfile)

    with open(hfile, "w") as hd, open(cfile, "w") as cd:
        hd.write(hcont)
        cd.write(ccont)

if __name__ == "__main__":
    v3f = vector.vec3f()
    v4f = vector.vec4f(funcType.funcList("lcons", "add", "sub", "smult"))
    mat44f = matrix.mat44f(funcType.funcList(
        "zero",
        "identity",
        ["mmult", "mat44f_mult", "mat44f", 4, 4],
        ["mmult", "mat44fv4_mult", "vec4f", 4, 1],
        "mat44perspective"
    ))
    genLinearLib("linear", [v3f, v4f, mat44f])
