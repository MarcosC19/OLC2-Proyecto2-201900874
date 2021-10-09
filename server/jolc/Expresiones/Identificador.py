from tablaSimbolos.Tipo import TIPO_DATO
from Excepciones.Excepcion import Excepcion
from Abstract.nodoAST import nodeAST
from Abstract.AST import AST
from Expresiones.Primitivo import Primitivo


class Identificador(AST):

    def __init__(self, type, line, column, identifier):
        super().__init__(type, line, column)
        self.identificador = identifier

    def getIdentifier(self):
        return self.identificador

    def getNode(self):
        node = nodeAST("IDENTIFICADOR")
        node.addChild(self.identificador)
        return node

    def interpretar(self, table, tree):
        simbolo = table.getVariable(self.identificador)
        if simbolo == None:
            return Excepcion("Semantico", "La variable " + str(self.identificador) + " no ha sido creada", self.line, self.column)
        self.type = simbolo.type
        if simbolo.type == TIPO_DATO.STRUCTN or simbolo.type == TIPO_DATO.STRUCTM or isinstance(simbolo.type, str):
            myStruct = simbolo
            return myStruct
        return simbolo.getValor()

    def getC3D(self):
        return ""