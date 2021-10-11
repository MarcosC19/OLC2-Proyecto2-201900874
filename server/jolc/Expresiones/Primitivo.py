from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.nodoAST import nodeAST
from Abstract.AST import AST


class Primitivo(AST):

    def __init__(self, type, line, column, value):
        super().__init__(type, line, column)
        self.value = value

    def getValue(self):
        return self.value

    def getNode(self):
        nodo = nodeAST("PRIMITIVO")
        if(self.type == TIPO_DATO.ENTERO):
            nodoT = nodeAST("ENTERO")
            nodoT.addChild(self.value)
            nodo.addChildrenNode(nodoT)
        elif(self.type == TIPO_DATO.DECIMAL):
            nodoT = nodeAST("DECIMAL")
            nodoT.addChild(self.value)
            nodo.addChildrenNode(nodoT)
        elif(self.type == TIPO_DATO.CADENA):
            nodoT = nodeAST("CADENA")
            nodoT.addChild("\"")
            nodoT.addChild(self.value)
            nodoT.addChild("\"")
            nodo.addChildrenNode(nodoT)
        elif(self.type == TIPO_DATO.CARACTER):
            nodoT = nodeAST("CARACTER")
            nodoT.addChild("\'")
            nodoT.addChild(self.value)
            nodoT.addChild("\'")
            nodo.addChildrenNode(nodoT)
        elif(self.type == TIPO_DATO.BOOLEANO):
            nodoT = nodeAST("BOOLEANO")
            nodoT.addChild(self.value)
            nodo.addChildrenNode(nodoT)
        elif(self.type == TIPO_DATO.LISTA):
            nodoT = nodeAST("LISTA")
            nodoT.addChild(self.value)
            nodo.addChildrenNode(nodoT)
        elif(self.type == TIPO_DATO.NULL):
            nodoT = nodeAST("NULL")
            nodoT.addChild(self.value)
            nodo.addChildrenNode(nodoT)
        elif(self.type == TIPO_DATO.ERROR):
            nodoT = nodeAST("ERROR")
            nodoT.addChild(self.value)
            nodo.addChildrenNode(nodoT)


        return nodo

    def interpretar(self, table, tree):
        if(isinstance(self.value, str)):        
            if self.value.lower() == 'true':
                return True
            elif self.value.lower() == 'false':
                return False
        return self.value

    def getC3D(self, contador):
        C3D = []
        if(isinstance(self.value, str)):        
            if self.value.lower() == 'true':
                for i in 'true':
                    C3D.append(ord(i))
            elif self.value.lower() == 'false':
                for i in 'false':
                    C3D.append(ord(i))
            else:
                for i in self.value:
                    C3D.append(ord(i))
        else:
            C3D.append(self.value)
        return C3D