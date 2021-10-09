from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion

class Pop(AST):

    def __init__(self, type, line, column, identifier):
        super().__init__(type, line, column)
        self.identificador = identifier

    def getNode(self):
        node = nodeAST("POP")
        node.addChild("pop!")
        node.addChild("(")
        node.addChild(self.identificador)
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        valores = table.getVariable(self.identificador)
        if valores.type == TIPO_DATO.LISTA:
            primitivo = valores.value
            lista = primitivo.value
            if len(lista) > 0:
                regreso = lista.pop()
                return regreso
            else:
                return Excepcion("Semantico", "La lista no tiene elementos que eliminar", self.line, self.column)
        else:
            return Excepcion("Semantico", "La variable no es de tipo lista", self.line, self.column)

    def getC3D(self):
        return ""