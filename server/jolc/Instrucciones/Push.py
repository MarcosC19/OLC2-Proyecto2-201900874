from Expresiones.Identificador import Identificador
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class Push(AST):

    def __init__(self, type, line, column, identifier, expression, access):
        super().__init__(type, line, column)
        self.identificador = identifier
        self.expresion = expression
        self.listaVals = None
        self.acceso = None
        if access != None:
            if isinstance(access, list):
                self.posicion = []
                for pos in access:
                    if isinstance(pos, list):
                        self.recorrer(pos)
                    else:
                        self.posicion.append(pos)
                self.acceso = self.posicion
            else:
                self.acceso = access

    def getNode(self):
        node = nodeAST("PUSH")
        node.addChild("push!")
        node.addChild("(")
        node.addChild(self.identificador)
        if self.acceso != None:
            if isinstance(self.acceso, list):
                for pos in self.acceso:
                    node.addChild("[")
                    node.addChildrenNode(pos.getNode())
                    node.addChild("]")
            else:
                node.addChild("[")
                node.addChildrenNode(self.acceso.getNode())
                node.addChild("]")
        node.addChild(",")
        if not isinstance(self.expresion, list):
            node.addChildrenNode(self.expresion.getNode())
        else:
            node.addChild("[")
            for valor in self.expresion:
                if self.listaVals != None:
                    node.addChild(self.listaVals)
                else:
                    node.addChildrenNode(valor.getNode())
                if valor != self.expresion[-1]:
                    node.addChild(",")
            node.addChild("]")
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        valores = table.getVariable(self.identificador)
        if valores.type == TIPO_DATO.LISTA:
            primitivo = valores.value
            lista = primitivo.value
            if self.acceso == None:
                if not isinstance(self.expresion, list):
                    if isinstance(self.expresion, Primitivo):
                        lista.append(self.expresion)
                        return None
                    else:
                        valor = self.expresion.interpretar(table, tree)
                        if not isinstance(valor, Primitivo):
                           valor = valor.interpretar(table, tree) 
                        lista.append(valor)
                else:
                    lista1 = self.expresion
                    lista1 = self.interList(lista1, table, tree)
                    lista.append(lista1)
                    self.listaVals = self.intList(lista, table, tree)
                    return None
            else:
                if isinstance(self.acceso, Primitivo):
                    position = self.acceso.interpretar(table, tree)
                    position = int(position - 1)
                    if not isinstance(self.expresion, list):
                        if isinstance(self.expresion, Primitivo):
                            lista[position].append(self.expresion)
                            return None
                        else:
                            valor = self.expresion.interpretar(table, tree)
                            lista[position].append(valor)
                    else:
                        lista1 = self.expresion
                        lista[position].append(lista1)
                        self.listaVals = self.intList(lista, table, tree)
                        return None
                elif isinstance(self.acceso, Identificador):
                    position = self.acceso.interpretar(table, tree)
                    position = position.interpretar(table, tree)
                    position = int(position - 1)
                    if not isinstance(self.expresion, list):
                        if isinstance(self.expresion, Primitivo):
                            lista[position].append(self.expresion)
                            return None
                        else:
                            valor = self.expresion.interpretar(table, tree)
                            if not isinstance(valor, Primitivo):
                                valor = valor.interpretar(table, tree) 
                            lista.append(valor)
                    else:
                        lista1 = self.expresion
                        lista1 = self.interList(lista1, table, tree)
                        lista[position].append(lista1)
                        self.listaVals = self.intList(lista, table, tree)
                        return None
                else:
                    for pos in self.acceso:
                        if isinstance(lista, list):
                            lista = self.valList(lista, table, tree, pos)
                        if isinstance(lista, Primitivo) and pos != self.acceso[-1]:
                            return Excepcion("Semantico", "La dimension ingresada no es valida", self.line, self.column)
                    if isinstance(self.expresion, Primitivo):
                        lista.append(self.expresion)
                        return None
                    else:
                        valor = self.expresion.interpretar(table, tree)
                        lista.append(valor)
                        self.listaVals = self.intList(lista, table, tree)
        else:
            return Excepcion("Semantico", "La variable no es de tipo lista", self.line, self.column)

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

    def recorrer(self, lista):
        arreglo = []
        for val in lista:
            if isinstance(val, list):
                reg = self.recorrer(val)
                arreglo.append(reg)
            else:
                self.posicion.append(val)