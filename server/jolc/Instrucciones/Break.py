from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO

class Break(AST):

    def __init__(self, line, column):
        super().__init__(TIPO_DATO.CADENA, line, column)

    def getNode(self):
        node = nodeAST("BREAK")
        node.addChild("break");
        node.addChild(";")
        return node

    def interpretar(self, table, tree):
        return self

    def getC3D(self, c3dObj, finalL):
        if finalL != None:
            C3D = "    /* EJECUCION BREAK */\n"
            C3D += "    goto L" + str(finalL) + ";\n"
            return C3D
        return ""