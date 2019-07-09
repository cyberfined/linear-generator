import funcType
import vector
from utils import typeLetter

compontents = ["X", "Y", "Z", "W"]

class Matrix:
    def __init__(self, rows, cols, scalar, funcs):
        self.rows = rows
        self.cols = cols
        self.num = rows*cols
        self.scalar = scalar
        self.funcs = funcs

        for f in funcs:
            f.args["rows"] = rows
            f.args["cols"] = cols
            f.args["lvec"] = self.getLowVectorType()

        funcs.insert(0, self.getConstructor())

        if self.rows > len(compontents):
            raise Exception("To many matrix components, add component name in matrix.py")

    def getType(self):
        return "mat" + str(self.rows) + str(self.cols) + typeLetter(self.scalar)

    def getVectorType(self):
        return vector.Vector(self.cols, self.scalar, []).getType()

    def getLowVectorType(self):
        return vector.Vector(self.cols-1, self.scalar, []).getType()

    def getConstructor(self):
        vec = self.getVectorType()
        var = [c for c in compontents[:self.rows]]
        defvar = map(lambda x: vec + " " + x, var)
        var = ", ".join(var)
        defvar = ", ".join(defvar)

        t = self.getType()
        name = t[0].upper() + t[1:]
        proto = "{0} {1}({2})".format(t, name, defvar)
        body = "{0} {{ return ({1}) {{ {2} }}; }}".format(proto, t, var);
        return funcType.ParticularFunc.manualCreate(name, proto+";", body)


    def getDefinition(self):
        template = "typedef struct {{ {0} {1}; }} {2};"
        var = ",".join([c for c in compontents[:self.rows]])
        return template.format(self.getVectorType(), var, self.getType())
    
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
