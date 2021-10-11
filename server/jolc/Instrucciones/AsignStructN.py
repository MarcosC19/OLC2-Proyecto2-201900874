from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion

class StructN(AST):

    def __init__(self, type, line, column, identifier, attributes):
        super().__init__(type, line, column)
        self.identificador = identifier
        self.atributos = attributes

    def getNode(self):
        node = nodeAST("STRUCT")
        if self.type == TIPO_DATO.STRUCTM:
            node.addChild("mutable")
        node.addChild("struct")
        node.addChild(self.identificador)
        nodeAtri = nodeAST("ATRIBUTOS")
        for atributo in self.atributos:
            nodeAtri.addChildrenNode(atributo.getNode())
        node.addChildrenNode(nodeAtri)
        node.addChild("end;")
        return node

    def interpretar(self, table, tree):
        variable = table.getVariable(self.identificador)
        if variable == None:
            simboloG = Simbolo(self.type, self.identificador, self.line, self.column, self.atributos)
            table.setVariable(simboloG)
            return None
        else:
            if variable.type != self.type:
                simboloG = Simbolo(self.type, self.identificador, self.line, self.column, self.atributos)
                table.setVariable(simboloG)
                return None
            else:
                return Excepcion("Semantico", "El struct " + self.identificador + " ya ha sido creado", self.line, self.column)

    def getC3D(self, contador):
        return ""