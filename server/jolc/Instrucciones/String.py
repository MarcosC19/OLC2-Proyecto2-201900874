from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class String(AST):

    def __init__(self, type, line, column, string):
        super().__init__(type, line, column)
        self.cadena = string

    def getNode(self):
        node = nodeAST("STRING")
        node.addChild("string")
        node.addChild("(")
        node.addChildrenNode(self.cadena.getNode())
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        valor = self.cadena.interpretar(table, tree)
        if isinstance(valor, Excepcion): return valor
        if isinstance(valor, Primitivo): 
            valor.type = self.type
            return valor
        return Primitivo(self.type, self.line, self.column, str(valor))

    def getC3D(self):
        return ""