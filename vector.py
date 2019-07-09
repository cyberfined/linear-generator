import funcType
from utils import typeLetter

def vec2i(funcs=[]): return Vector(2, "int", funcs)
def vec2f(funcs=[]): return Vector(2, "float", funcs)
def vec2d(funcs=[]): return Vector(2, "double", funcs)

def vec3i(funcs=[]): return Vector(3, "int", funcs)
def vec3f(funcs=[]): return Vector(3, "float", funcs)
def vec3d(funcs=[]): return Vector(3, "double", funcs)

def vec4i(funcs=[]): return Vector(4, "int", funcs)
def vec4f(funcs=[]): return Vector(4, "float", funcs)
def vec4d(funcs=[]): return Vector(4, "double", funcs)

compontents = ["x", "y", "z", "w"]

class Vector:
    def __init__(self, num, scalar, funcs):
        self.num = num
        self.scalar = scalar
        self.funcs = funcs

        for f in funcs:
            f.args["lvec"] = self.getLowVectorType()

        funcs.insert(0, self.getConstructor())

        if self.num > len(compontents):
            raise Exception("To many vector components, add component name in vector.py")

    def getType(self):
        return "vec" + str(self.num) + typeLetter(self.scalar)

    def getLowVectorType(self):
        return "vec" + str(self.num-1) + typeLetter(self.scalar)

    def getConstructor(self):
        var = [c for c in compontents[:self.num]]
        defvar = map(lambda x: self.scalar + " " + x, var)
        var = ", ".join(var)
        defvar = ", ".join(defvar)

        t = self.getType()
        name = t[0].upper() + t[1:]
        proto = "{0} {1}({2})".format(t, name, defvar)
        body = "{0} {{ return ({1}) {{ {2} }}; }}".format(proto, t, var);
        return funcType.ParticularFunc.manualCreate(name, proto+";", body)

    def getDefinition(self):
        template = "typedef struct {{ {0} {1}; }} {2};"
        var = ','.join([c for c in compontents[:self.num]])
        return template.format(self.scalar, var, self.getType())

    def getSize(self):
        return self.num

    def getScalar(self):
        return self.scalar

    def getGenericFuncs(self):
        funcs = []
        for f in self.funcs:
            funcs.extend(f.getDeps())
        return funcs

    def getParticularFuncs(self):
        return self.funcs
