from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO

class Truncate(AST):

    def __init__(self, line, column, string, type = None):
        super().__init__(type, line, column)
        self.cadena = string

    def getNode(self):
        node = nodeAST("TRUNC")
        node.addChild("trunc")
        node.addChild("(")
        if self.type != None:
            if self.type == TIPO_DATO.ENTERO: node.addChild("Int64")
            elif self.type == TIPO_DATO.DECIMAL: node.addChild("Float64")
            node.addChild(",")
        node.addChildrenNode(self.cadena.getNode())
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        valor = self.cadena.interpretar(table, tree)
        if isinstance(valor, Excepcion): return valor
        if self.type != None:
            if isinstance(valor, float):
                return Primitivo(self.type, self.line, self.column, int(valor))
        else:
            if isinstance(valor,float):
                return Primitivo(TIPO_DATO.DECIMAL, self.line, self.column, int(valor))
        return Excepcion("Semantico", "Se esperaba un tipo Float64", self.line, self.column)

    def getC3D(self):
        return ""