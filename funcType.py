import particularGenerators
import genericGenerators
import copy

def funcList(*lst):
    res = []
    for l in lst:
        if type(l) is str:
            res.append(particularFuncs[l]())
        else:
            res.append(particularFuncs[l[0]](*l[1:]))
    return res

class ParticularFunc:
    def __init__(self, name, args=dict()):
        self.name = name
        self.args = args

    @staticmethod
    def manualCreate(name, proto, body, args=dict(), deps=[]):
        pf = copyC(name, args)
        pf.getProto = lambda *args: proto
        pf.getBody = lambda *args: body
        pf.getDeps = lambda *args: deps
        return pf

    def getProto(self, vec, scalar):
        return particularGenerators.funcProto(vec, scalar, self.name, **self.args)

    def getBody(self, vec, scalar, size):
        return particularGenerators.funcBody(vec, scalar, self.name, size, **self.args)

    def getDeps(self):
        if self.name not in genericFuncs: return []
        gf = genericFuncs[self.name]
        deps = gf.getDeps()
        deps.append(gf)
        return deps

class GenericFunc:
    def __init__(self, name, deps=[]):
        self.name = name
        self.deps = deps

    def getBody(self, scalar):
        return genericGenerators.funcBody(scalar, self.name)

    def getDeps(self):
        deps = []
        for d in self.deps:
            gf = genericFuncs[d]
            deps.extend(gf.getDeps())
            deps.append(gf)
        return deps

def copyC(*args): return copy.deepcopy(ParticularFunc(*args))
particularFuncs = {
        "zero": lambda: copyC("zero"),
        "identity": lambda: copyC("identity"),
        "transpose": lambda: copyC("transpose"),
        "mmult": lambda name, rtype, r2, c2: copyC("mmult", {"func": name, "rtype": rtype, "r2": r2, "c2": c2}),
        "translate": lambda: copyC("translate"),
        "scale": lambda: copyC("scale"),
        "mat44rotate": lambda: copyC("mat44rotate"),
        "mat44perspective": lambda: copyC("mat44perspective"),
        "add": lambda: copyC("add"),
        "sub": lambda: copyC("sub"),
        "smult": lambda: copyC("smult"),
        "interpolate": lambda: copyC("interpolate"),
        "dot": lambda: copyC("dot"),
        "vec3cross": lambda: copyC("vec3cross"),
        "sqlength": lambda: copyC("sqlength"),
        "length": lambda: copyC("length"),
        "normalize": lambda: copyC("normalize"),
        "proj": lambda: copyC("proj"),
        "hom": lambda: copyC("hom")
}

genericFuncs = {
        "zero": GenericFunc("zero"),
        "identity": GenericFunc("identity", ["zero"]),
        "transpose": GenericFunc("transpose"),
        "mmult": GenericFunc("mmult"),
        "translate": GenericFunc("translate", ["identity"]),
        "scale": GenericFunc("scale", ["identity"]),
        "add": GenericFunc("add"),
        "sub": GenericFunc("sub"),
        "smult": GenericFunc("smult"),
        "interpolate": GenericFunc("interpolate", ["add", "sub", "smult"]),
        "dot": GenericFunc("dot"),
        "sqlength": GenericFunc("sqlength", ["dot"]),
        "length": GenericFunc("length", ["sqlength"]),
        "normalize": GenericFunc("normalize", ["length"]),
        "proj": GenericFunc("proj"),
        "hom": GenericFunc("hom")
}
