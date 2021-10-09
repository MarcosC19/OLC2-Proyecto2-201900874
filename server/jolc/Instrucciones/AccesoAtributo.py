from Expresiones.Primitivo import Primitivo
from tablaSimbolos.Simbolo import Simbolo
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Excepciones.Excepcion import Excepcion

class AccesoAtributo(AST):

    def __init__(self, type, line, column, identifierS, identifierA):
        super().__init__(type, line, column)
        self.identificadorS = identifierS
        self.identificadorA = identifierA

    def getNode(self):
        node = nodeAST("ACCESO STRUCT")
        if isinstance(self.identificadorS, AccesoAtributo):
            node.addChildrenNode(self.identificadorS.getNode())
        else:
            node.addChild(self.identificadorS)
        node.addChild(".")
        node.addChild(self.identificadorA)
        return node

    def interpretar(self, table, tree):
        if not isinstance(self.identificadorS, AccesoAtributo):
            myStruct = table.getVariable(self.identificadorS)
            if myStruct != None:
                self.type = myStruct.type
                myValue = myStruct.getValor().interpretar(table, tree)
                myAttributes = myValue.getValor()
                if not isinstance(myAttributes, list):
                    myAttributes = self.recorrerLista(myAttributes, table, tree)
                atTrabajar = None
                for atributo in myAttributes:
                    if atributo.identificador == self.identificadorA:
                        atTrabajar = atributo
                        break
                if atTrabajar == None:
                    return Excepcion("Semantico", "El atributo " + self.identificadorA + " no existe", self.line, self.column)
                else:
                    return atTrabajar.getValor()
            else:
                return Excepcion("Semantico", "El struct " + self.identificadorS + " no ha sido creado", self.line, self.column)
        else:
            myStruct = self.identificadorS.interpretar(table, tree)
            if isinstance(myStruct, Excepcion): return myStruct
            if isinstance(myStruct, Simbolo):
                valores = myStruct.getValor()
                if not isinstance(valores, list):
                    valores = self.recorrerLista(valores, table, tree)
                atTrabajar = None
                for atributo in valores:
                    if atributo.identificador == self.identificadorA:
                        atTrabajar = atributo
                        break
                if atTrabajar == None:
                    return Excepcion("Semantico", "El atributo " + self.identificadorA + " no existe", self.line, self.column)
                else:
                    return atTrabajar.getValor()
            else:
                otherStruct = myStruct.interpretar(table, tree)
                if isinstance(otherStruct, Simbolo):
                    valores = otherStruct.getValor()
                    atTrabajar = None
                    for atributo in valores:
                        if atributo.identificador == self.identificadorA:
                            atTrabajar = atributo
                            break
                    if atTrabajar == None:
                        return Excepcion("Semantico", "El atributo " + self.identificadorA + " no existe", self.line, self.column)
                    else:
                        return atTrabajar.getValor()
            if isinstance(myStruct, Primitivo):
                return Excepcion("Semantico", "El atributo " + self.identificadorA + " no existe", self.line, self.column)

    def getC3D(self):
        return ""
        
    def recorrerLista(self, lista, table, tree):
        valorL = None
        if isinstance(lista, Primitivo):
            valorL = lista.interpretar(table, tree)
        elif isinstance(lista, Simbolo):
            valorL = lista.getValor()
        
        if not isinstance(valorL, list):
            valorL = self.recorrerLista(valorL, table, tree)
        
        return valorL
