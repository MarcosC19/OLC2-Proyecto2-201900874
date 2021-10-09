from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class Continue(AST):

    def __init__(self, line, column):
        super().__init__(TIPO_DATO.CADENA, line, column)

    def getNode(self):
        node = nodeAST("CONTINUE")
        node.addChild("continue")
        node.addChild(";")
        return node

    def interpretar(self, table, tree):
        return self

    def getC3D(self):
        return ""