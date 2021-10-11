from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO

class Float(AST):

    def __init__(self, line, column, string, type = None):
        super().__init__(type, line, column)
        self.cadena = string

    def getNode(self):
        node = nodeAST("FLOAT")
        node.addChild("float")
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
            if isinstance(valor, int):
                return Primitivo(self.type, self.line, self.column, float(valor))
        else:
            if isinstance(valor, int):
                return Primitivo(TIPO_DATO.DECIMAL, self.line, self.column, float(valor))
        return Excepcion("Semantico", "Se esperaba un tipo Int64", self.line, self.column)

    def getC3D(self, contador):
        return ""