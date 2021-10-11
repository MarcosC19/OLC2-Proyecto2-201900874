from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class Atributo(AST):

    def __init__(self, line, column, identifier, value, type):
        super().__init__(type, line, column)
        self.identificador = identifier
        self.valor = value

    def setValor(self, value):
        self.valor = value

    def getValor(self):
        return self.valor

    def getNode(self):
        node = nodeAST("ATRIBUTO")
        node.addChild(self.identificador)
        if self.type != None:
            node.addChild("::")
            if self.type == TIPO_DATO.ENTERO: node.addChild("Int64")
            elif self.type == TIPO_DATO.DECIMAL: node.addChild("Float64")
            elif self.type == TIPO_DATO.CADENA: node.addChild("String")
            elif self.type == TIPO_DATO.CARACTER: node.addChild("Char")
            elif self.type == TIPO_DATO.BOOLEANO: node.addChild("Boolean")
            elif self.type == TIPO_DATO.LISTA: node.addChild("List")
            elif self.type == TIPO_DATO.NULL: node.addChild("Null")
        if self.valor != None:
            node.addChild("=")
            node.addChildrenNode(self.valor.getNode())
        node.addChild(";")
        return node

    def interpretar(self, table, tree):
        return self

    def getC3D(self, contador):
        return ""