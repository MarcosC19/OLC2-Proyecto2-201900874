from Instrucciones.AsignacionVar import Asignacion
from Expresiones.Primitivo import Primitivo
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO

class Parametro(AST):

    def __init__(self, line, column, identifier, type):
        super().__init__(type, line, column)
        self.identificador = identifier

    def getNode(self):
        node = nodeAST("PARAMETRO")
        node.addChildrenNode(self.identificador)
        node.addChild("::")
        if self.type == TIPO_DATO.ENTERO: node.addChild("Int64")
        if self.type == TIPO_DATO.DECIMAL: node.addChild("Float64")
        if self.type == TIPO_DATO.CARACTER: node.addChild("Char")
        if self.type == TIPO_DATO.CADENA: node.addChild("String")
        if self.type == TIPO_DATO.BOOLEANO: node.addChild("Bool")
        if self.type == TIPO_DATO.LISTA: node.addChild("Lista")
        if self.type == TIPO_DATO.NULL: node.addChild("Null")
        return node

    def interpretar(self, table, tree):
        return self

    def getC3D(self, c3dObj):
        return ""