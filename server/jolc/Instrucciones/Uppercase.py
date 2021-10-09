from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion

class UpperCase(AST):

    def __init__(self, type, line, column, expression):
        super().__init__(type, line, column)
        self.expresion = expression

    def getNode(self):
        node = nodeAST("UPPERCASE")
        node.addChild("uppercase")
        node.addChild("(")
        node.addChildrenNode(self.expresion.getNode())
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        if self.expresion.type == TIPO_DATO.CADENA or self.expresion.type == TIPO_DATO.CARACTER:
            self.type = self.expresion.type
            value = self.expresion.interpretar(table, tree)
            if isinstance(value, Excepcion): return value
            if isinstance(value, Primitivo): value = value.interpretar(table, tree)
            return str(value).upper()
        else:
            return Excepcion("Semantico", "Se esperaba una cadena o caracter", self.line, self.column)

    def getC3D(self):
        return ""