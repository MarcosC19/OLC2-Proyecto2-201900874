from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class Typeof(AST):

    def __init__(self, type, line, column, expression):
        super().__init__(type, line, column)
        self.expresion = expression

    def getNode(self):
        node = nodeAST("TYPEOF")
        node.addChild("typeof")
        node.addChild("(")
        node.addChildrenNode(self.expresion.getNode())
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        valor = self.expresion.interpretar(table, tree)
        if isinstance(valor, Excepcion): return valor
        self.type = self.expresion.type
        if self.expresion.type == TIPO_DATO.ENTERO: return 'Int64'
        elif self.expresion.type == TIPO_DATO.DECIMAL: return 'Float64'
        elif self.expresion.type == TIPO_DATO.CARACTER: return 'Char'
        elif self.expresion.type == TIPO_DATO.CADENA: return 'String'
        elif self.expresion.type == TIPO_DATO.BOOLEANO: return 'Bool'
        elif self.expresion.type == TIPO_DATO.NULL: return 'Null'

    def getC3D(self, contador):
        return ""