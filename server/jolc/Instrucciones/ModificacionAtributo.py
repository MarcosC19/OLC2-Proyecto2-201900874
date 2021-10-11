from Expresiones.Primitivo import Primitivo
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Simbolo import Simbolo

class ModiAtributo(AST):

    def __init__(self, type, line, column, identifierS,  identifierA, expression):
        super().__init__(type, line, column)
        self.identificadorS = identifierS
        self.identificadorA = identifierA
        self.expresion = expression

    def getNode(self):
        node = nodeAST("MODIFICAR STRUCT")
        node.addChild(self.identificadorS)
        node.addChild(".")
        node.addChild(self.identificadorA)
        node.addChild("=")
        node.addChildrenNode(self.expresion.getNode())
        return node

    def interpretar(self, table, tree):
        myStruct = table.getVariable(self.identificadorS)
        if myStruct != None:
            self.type = myStruct.type
            if myStruct.type == TIPO_DATO.STRUCTM:
                myValue = myStruct.getValor().interpretar(table, tree)
                myAttributes = None
                if isinstance(myValue, Simbolo):
                    myAttributes = self.recorrerSimbolo(myValue.getValor(), table, tree)
                elif isinstance(myValue, Primitivo):
                    myAttributes = self.recorrerSimbolo(myValue.interpretar(table, tree), table, tree)
                else:
                    myAttributes = myValue.atributos
                atTrabajar = None
                indice = None
                for atributo in myAttributes:
                    if atributo.identificador == self.identificadorA:
                        atTrabajar = atributo
                        indice = myAttributes.index(atributo)
                        break
                if atTrabajar == None:
                    return Excepcion("Semantico", "El atributo " + self.identificadorA + " no existe", self.line, self.column)
                else:
                    if isinstance(self.expresion, Primitivo):
                        if atTrabajar.type != None:
                            if self.expresion.type == atTrabajar.type:
                                myAttributes[indice].valor = self.expresion
                                return None
                            else:
                                return Excepcion("Semantico", "Los tipos deben ser los mismos", self.line, self.column)
                        else:
                            myAttributes[indice] = self.expresion
                            return None
            else:
                return Excepcion("Semantico", "El struct " + self.identificadorS + " no es modificable", self.line, self.column)
        else:
            return Excepcion("Semantico", "El struct " + self.identificadorS + " no ha sido creado", self.line, self.column)

    def recorrerSimbolo(self, valor, table, tree):
        if isinstance(valor, list):
            return valor
        else:
            if isinstance(valor, Simbolo):
                valor = self.recorrerSimbolo(valor.getValor(), table ,tree)
            elif isinstance(valor, Primitivo):
                valor = self.recorrerSimbolo(valor.interpretar(table,tree), table, tree)
            return valor

    def getC3D(self, contador):
        return ""