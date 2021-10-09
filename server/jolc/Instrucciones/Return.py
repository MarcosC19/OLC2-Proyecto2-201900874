from Expresiones.Primitivo import Primitivo
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class Return(AST):

    def __init__(self, line, column, expression):
        super().__init__(TIPO_DATO.NULL, line, column)
        self.expresion = expression

    def getNode(self):
        node = nodeAST("RETURN")
        node.addChild("return")
        node.addChildrenNode(self.expresion.getNode())
        node.addChild(";")
        return node

    def interpretar(self, table, tree):
        if isinstance(self.expresion, Primitivo):
            return self.expresion
        else:
            return self.expresion.interpretar(table, tree)

    def getC3D(self):
        return ""