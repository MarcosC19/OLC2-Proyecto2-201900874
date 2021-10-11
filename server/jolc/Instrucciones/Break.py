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

    def getC3D(self, contador):
        return ""