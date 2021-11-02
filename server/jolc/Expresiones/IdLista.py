from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO
from C3D.variableC3D import TipoVariable

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

    def getC3D(self, c3dObj):
        # ((i - 1)* N2 + j - 1)* N3 + k - 1
        C3D = "    /* ACCEDIENDO A LISTA */\n"
        myLista = c3dObj.getVariable(self.identificador)
        listado = myLista.tamanios.copy()
        valPos = listado.copy()
        Pos0 = valPos[0][0]
        valPos.pop(0)
        numPos = 0
        dimension = 0
        temporalSUM = 0
        temporalENV = 0
        temporalULT = []
        C3D += "    t" + str(c3dObj.getContadorT()) + " = " + myLista.getPosition() + ";\n"
        c3dObj.addContadorT()
        C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(c3dObj.getLastContadorT()) + ")];\n"
        temporalAsig = c3dObj.getContadorT()
        c3dObj.addContadorT()
        if myLista != None and myLista.getTypeVariable() == TipoVariable.LISTA:
            for posicion in self.posicion: # CALCULANDO POSICION
                if numPos == 0:
                    if isinstance(posicion, Primitivo):
                        valor = posicion.getValue()
                        resBE = c3dObj.printBoundsError(valor, Pos0)
                        C3D += resBE[0]
                        temporalULT.append(resBE[1])
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = " + str(valor) + " - 1;\n"
                        temporalSUM = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        numPos = valor
                    else:
                        resultado = posicion.getC3D(c3dObj)
                        C3D += resultado[0]
                        resBE = c3dObj.printBoundsError("t" + str(resultado[1]), Pos0)
                        C3D += resBE[0]
                        temporalULT.append(resBE[1])
                        variable = resultado[2]
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(resultado[1]) + " - 1;\n"
                        temporalSUM = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        numPos += 1

                    dimension += 1
                else:
                    if isinstance(posicion, Primitivo):
                        if len(valPos) > numPos:
                            numPos -= 1
                            valPos3 = valPos.pop(numPos)
                            valor = posicion.getValue()
                            valPos2 = valPos3[0]
                            resBE = c3dObj.printBoundsError(valor, valPos2[dimension])
                            C3D += resBE[0]
                            temporalULT.append(resBE[1])
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalSUM) + " * " + str(valPos2[dimension])  +";\n"
                            temporalA1 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalA1) + " + " + str(valor) + ";\n"
                            temporalA2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalA2) + " - 1;\n"
                            temporalSUM = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            numPos = valor
                        valPos.pop(0)
                    else:
                        longitud = 0
                        for value in valPos:
                            print(value)
                            if isinstance(value, list):
                                if value[0][dimension] > longitud:
                                    longitud = value[0][dimension]
                            else:
                                if value[dimension] > longitud:
                                    longitud = value[dimension]
                        resultado = posicion.getC3D(c3dObj)
                        C3D += resultado[0]
                        resBE = c3dObj.printBoundsError("t" + str(resultado[1]), longitud)
                        C3D += resBE[0]
                        temporalULT.append(resBE[1])
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalSUM) + " * " + str(longitud)  +";\n"
                        temporalA1 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalA1) + " + t" + str(resultado[1]) + ";\n"
                        temporalA2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalA2) + " - 1;\n"
                        temporalSUM = c3dObj.getContadorT()
                        c3dObj.addContadorT()

                        nuevoPos = []
                        for value in valPos:
                            if len(value) > len(nuevoPos):
                                if len(value) == 1:
                                    if isinstance(value, list):
                                        nuevoPos = value[0]
                                    else:
                                        nuevoPos = []
                                else:
                                    if isinstance(value, list):
                                        nuevoPos = value[1]
                                    else:
                                        nuevoPos = []
                        valPos = nuevoPos
                        print(nuevoPos)
                        numPos += 1
                    dimension += 1

            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAsig) + " + t" + str(temporalSUM)  +";\n"
            temporalF = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += "    t" + str(c3dObj.getContadorT()) + " = heap[int(t" + str(temporalF) +")];\n"
            temporalENV = c3dObj.getContadorT()
            c3dObj.addContadorT()
        return [C3D, temporalENV, temporalULT]
    
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