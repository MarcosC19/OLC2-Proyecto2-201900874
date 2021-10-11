from Expresiones.Primitivo import Primitivo
from tablaSimbolos.Tipo import TIPO_DATO
from Instrucciones.AsignacionVar import Asignacion
from Abstract.nodoAST import nodeAST
from Abstract.AST import AST

class Lista(AST):

    def __init__(self, type, line, column, id, listVals):
        super().__init__(type, line, column)
        self.identificador = id
        self.listaVals = listVals

    def getNode(self):
        node = nodeAST("LISTA")
        node.addChild(self.identificador)
        node.addChild("=")
        if isinstance(self.listaVals, list):
            node.addChild(self.listaVals)
        else:
            node.addChild("[")
            node.addChildrenNode(self.listaVals.getNode())
            node.addChild("]")
        return node
    
    def interpretar(self, table, tree):
        valores = self.listaVals
        valores = self.interList(valores, table, tree)
        self.listaVals = self.intList(valores, table, tree)
        asignar = Asignacion(self.line, self.column, self.identificador, Primitivo(TIPO_DATO.LISTA, self.line, self.column, valores)).interpretar(table, tree)
        if asignar != None:
            return asignar
        return None

    def getC3D(self, contador):
        return ""
        
    def intList(self, lista, table, tree):
        valores = []
        for valor in lista:
            if isinstance(valor, list):
                valores.append(self.intList(valor, table, tree))
            else:
                valores.append(valor.interpretar(table, tree))
        return valores

    def interList(self, lista, table, tree):
        valores = []
        for valor in lista:
            if isinstance(valor, list):
                valores.append(self.interList(valor, table, tree))
            else:
                if isinstance(valor, Primitivo):
                    valores.append(valor)
                else:
                    valores.append(valor.interpretar(table, tree))
        return valores