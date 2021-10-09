from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO
from Excepciones.Excepcion import Excepcion
from Expresiones.Primitivo import Primitivo
from tablaSimbolos.Simbolo import Simbolo

class Global(AST):

    def __init__(self, line, column, identifier, expression):
        super().__init__(TIPO_DATO.NULL, line, column)
        self.identificador = identifier
        self.expresion = expression

    def getNode(self):
        node = nodeAST("GLOBAL")
        node.addChild("global")
        node.addChild(self.identificador)
        if self.expresion != None:
            node.addChild("=")
            node.addChildrenNode(self.expresion.getNode())
        return node

    def interpretar(self, table, tree):
        globalTable = table
        while globalTable != None:
            if globalTable.anterior != None:
                globalTable = globalTable.anterior
            else:
                break

        simbolo = None
        if self.identificador in globalTable.tabla:
            if self.expresion != None:
                value = self.expresion.interpretar(globalTable, tree)
                if isinstance(value, Excepcion): return value
                if isinstance(value, Primitivo):
                    self.type = value.type
                    simbolo = Simbolo(self.type, self.identificador, self.line, self.column, value)
                else:
                    self.type = self.expresion.type
                    valor = Primitivo(self.expresion.type, self.line, self.column, value)
                    simbolo = Simbolo(self.type, self.identificador, self.line, self.column, valor)
                globalTable.tabla[self.identificador] = simbolo

        return globalTable

    def getC3D(self):
        return ""