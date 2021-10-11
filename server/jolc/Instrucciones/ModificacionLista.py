from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import TIPO_DATO

class ModLista(AST):

    def __init__(self, type, line, column, identifier, position, expression):
        super().__init__(type, line, column)
        self.identificador = identifier
        self.posicion = []
        for pos in position:
            if isinstance(pos, list):
                self.recorrer(pos)
            else:
                self.posicion.append(pos)
        self.expresion = expression

    def getNode(self):
        node = nodeAST("MODIFICACION LISTA")
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
        node.addChild("=")
        if not isinstance(self.expresion, list):
            node.addChildrenNode(self.expresion.getNode())
        else:
            node.addChild("[")
            for valor in self.expresion:
                node.addChildrenNode(valor.getNode())
                if valor != self.expresion[-1]:
                    node.addChild(",")
            node.addChild("]")
        return node

    def interpretar(self, table, tree):
        valores = table.getVariable(self.identificador)
        if valores.type == TIPO_DATO.LISTA:
            primitivo = valores.value
            lista = primitivo.value
            if isinstance(self.posicion, Primitivo):
                valor = self.posicion.interpretar(table, tree)
                lista[int(valor)] = self.expresion
                print(lista)
            else:
                myLista = self.modConj(lista, self.posicion, self.expresion, table, tree)
                return None
        else:
            return Excepcion("Semantico", "La variable no es de tipo lista", self.line, self.column)

    def getC3D(self, contador):
        return ""
        
    def modConj(self, lista, posicion, valor, table, tree):
        for pos in posicion:
            if pos == posicion[-1]:
                value = pos.interpretar(table, tree)
                if isinstance(value, Primitivo):
                    value = self.primitivo(value, table, tree)
                value = int(value - 1)
                if isinstance(valor, Primitivo):
                    lista[value] = valor
                elif isinstance(valor, list):
                    lista[value] = valor
                else:
                    expres = valor.interpretar(table, tree)
                    if expres.type == TIPO_DATO.LISTA:
                        expres = expres.interpretar(table, tree)
                    lista[value] = expres
                return lista
            else:
                value = pos.interpretar(table, tree)
                if isinstance(value, Primitivo):
                    value = self.primitivo(value, table, tree)
                value = int(value - 1)
                lista = lista[value]

    def recorrer(self, lista):
        arreglo = []
        for val in lista:
            if isinstance(val, list):
                reg = self.recorrer(val)
                arreglo.append(reg)
            else:
                self.posicion.append(val)

    def primitivo(self, valor, table, tree):
        value = valor.interpretar(table, tree)
        if isinstance(value, Primitivo):
            value = self.primitivo(value, table, tree)
        return value