from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
import re

patron = re.compile('[a-zA-Z]+')

class Parse(AST):
    
    def __init__(self, line, column, string, type = None):
        super().__init__(type, line, column)
        self.cadena = string

    def getNode(self):
        node = nodeAST("PARSEO")
        node.addChild("parse")
        node.addChild("(")
        if self.type != None:
            if self.type == TIPO_DATO.ENTERO: node.addChild("Int64")
            elif self.type == TIPO_DATO.DECIMAL: node.addChild("Float64")
            node.addChild(",")
        node.addChildrenNode(self.cadena.getNode())
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        if self.type == None:
            if self.cadena.type == TIPO_DATO.CADENA:
                valor = self.cadena.interpretar(table, tree)
                if isinstance(valor, Excepcion): return valor
                if patron.search(valor):
                    return Excepcion("Semantico", "Se esperaban valores numericos", self.line, self.column)
                if '.' in valor:
                    return Primitivo(TIPO_DATO.DECIMAL, self.line, self.column, float(valor))
                return Primitivo(TIPO_DATO.ENTERO, self.line, self.column, int(valor))
            else:
                return Excepcion("Semantico", "Se esperaba una cadena de texto", self.line, self.column)
        else:
            if self.cadena.type == TIPO_DATO.CADENA:
                valor = self.cadena.interpretar(table, tree)
                if isinstance(valor, Excepcion): return valor
                if patron.search(valor):
                    return Excepcion("Semantico", "Se esperaban valores numericos", self.line, self.column)
                if self.type == TIPO_DATO.ENTERO:
                    if '.' in valor:
                        return Excepcion("Semantico", "No es posible convertir a entero", self.line, self.column)
                    return Primitivo(TIPO_DATO.ENTERO, self.line, self.column, int(valor))
                elif self.type == TIPO_DATO.DECIMAL:
                    return Primitivo(TIPO_DATO.DECIMAL, self.line, self.column, float(valor))
                else:
                    return Excepcion("Semantico", "El tipo ingresado no es valido", self.line, self.column)
            else:
                return Excepcion("Semantico", "Se esperaba una cadena de texto", self.line, self.column)

    def getC3D(self):
        return ""