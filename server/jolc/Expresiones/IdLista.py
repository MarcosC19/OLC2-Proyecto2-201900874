from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO

class IdLista(AST):

    def __init__(self, type, line, column, identifier, number):
        super().__init__(type, line, column)
        self.identificador = identifier
        self.posicion = []
        for pos in number:
            if isinstance(pos, list):
                self.recorrer(pos)
            else:
                self.posicion.append(pos)

    def getNode(self):
        node = nodeAST("IDENTIFICADOR")
        node.addChild(self.identificador)
        if not isinstance(self.posicion, list):
            node.addChild("[")
            node.addChildrenNode(self.posicion.getNode())
            node.addChild("]")
        else:
            for pos in self.posicion:
                node.addChild("[")
                node.addChildrenNode(pos.getNode())
                node.addChild("]")
        return node

    def interpretar(self, table, tree):
        if isinstance(self.posicion, Primitivo):
            position = self.posicion.interpretar(table, tree)
            simbolo = table.getVariable(self.identificador)
            if simbolo == None:
                return Excepcion("Semantico", "La variable " + str(self.identificador) + " no ha sido creada", self.line, self.column)
            if simbolo.type != TIPO_DATO.LISTA:
                return Excepcion("Semantico", "La variable " + str(self.identificador) + " no es una lista", self.line, self.column)
            self.type = simbolo.type
            valores = simbolo.getValor()
            if int(position) > len(valores.value):
                return Excepcion("Semantico", "Indice fuera de rango", self.line, self.column)
            valorR = valores.value[int(position) - 1]
            if isinstance(valorR, list):
                valorR = self.recorrerLista(valorR, table, tree)
            return valorR
        else:
            simbolo = table.getVariable(self.identificador)
            if simbolo == None:
                return Excepcion("Semantico", "La variable " + str(self.identificador) + " no ha sido creada", self.line, self.column)
            if simbolo.type != TIPO_DATO.LISTA:
                return Excepcion("Semantico", "La variable " + str(self.identificador) + " no es una lista", self.line, self.column)
            self.type = simbolo.type
            valores = simbolo.getValor().value
            
            for pos in self.posicion:
                if isinstance(valores, list):
                    valores = self.valList(valores, table, tree, pos)
                if isinstance(valores, Primitivo) and pos != self.posicion[-1]:
                    return Excepcion("Semantico", "La dimension ingresada no es valida", self.line, self.column)
            if isinstance(valores, list):
                valores = self.recorrerLista(valores, table, tree)
            return valores    

    def getC3D(self, contador):
        return ""
        
    def recorrerLista(self, lista, table, tree):
        arreglo = []
        for val in lista:
            if isinstance(val, list):
                reg = self.recorrerLista(val, table, tree)
                arreglo.append(reg)
            else:
                arreglo.append(val)
        return arreglo

    def valList(self, lista, table, tree, posicion):
        position = posicion.interpretar(table, tree)
        if isinstance(position, Excepcion): return position
        if isinstance(position, Primitivo): position = position.interpretar(table, tree)
        if int(position) > len(lista):
            return Excepcion("Semantico", "Indice fuera de rango", self.line, self.column)
        valorR = lista[int(position) - 1]
        return valorR

    def recorrer(self, lista):
        arreglo = []
        for val in lista:
            if isinstance(val, list):
                reg = self.recorrer(val)
                arreglo.append(reg)
            else:
                self.posicion.append(val)