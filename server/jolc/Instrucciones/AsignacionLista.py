from Expresiones.Primitivo import Primitivo
from tablaSimbolos.Tipo import TIPO_DATO
from Instrucciones.AsignacionVar import Asignacion
from Abstract.nodoAST import nodeAST
from Abstract.AST import AST
from C3D.variableC3D import VariableC3D
from C3D.variableC3D import TipoVar
from C3D.variableC3D import TipoVariable

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

    def getC3D(self, c3dObj):
        C3D = "    /* CREANDO ARREGLO */\n"
        myNewVariable = None
        tamanios = []
        secondT = []
        dimension = 0
        temporalT0 = ""
        tamanio0 = 0
        myVarOld = c3dObj.getVariable(self.identificador)
        if myVarOld == None:
            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
            temporalTPos = c3dObj.getContadorT()
            c3dObj.addContadorT()
            c3dObj.addNumVariable()
            C3D += "    t" + str(c3dObj.getContadorT()) + " = H;\n"
            temporalHEAP = c3dObj.getContadorT()
            c3dObj.addContadorT()

            for valor in self.listaVals:
                tamanio0 += 1
                if isinstance(valor, Primitivo):
                    resultadoC3D = valor.getC3D(c3dObj)
                    if valor.type != TIPO_DATO.CADENA:
                        for value in resultadoC3D:
                            C3D += "    heap[int(H)] = " + str(value) + ";\n"
                            C3D += "    H = H + 1;\n"
                        self.type = TIPO_DATO.DECIMAL
                    else:
                        C3D += resultadoC3D
                        C3D += "    heap[int(H)] = 32;\n"
                        C3D += "    H = H + 1;\n"
                        self.type = TIPO_DATO.CADENA
                else:
                    if not isinstance(valor, list):
                        resultadoC3D = valor.getC3D(c3dObj)
                        C3D += resultadoC3D[0]
                        C3D += "    heap[int(H)] = t" + str(resultadoC3D[1]) + ";\n"
                        C3D += "    H = H + 1;\n"
                    else:
                        listaN = self.recorrerC3D(valor, c3dObj, secondT, dimension)
                        C3D += listaN[0]
                        secondT.append(listaN[1])
                        secondT = secondT[::-1]
            secondT.append({0:tamanio0})
            tamanios = secondT[::-1]
            C3D += "    heap[int(H)] = -1;\n"
            C3D += "    H = H + 1;\n"
            C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(temporalHEAP) + ";\n"
            myNewVariable = VariableC3D(self.identificador, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.APUNTADOR, self.type, TipoVariable.LISTA, self.line, self.column)
            
            myNewVariable.setTam(tamanios)
        else:
            C3D += "    t" + str(c3dObj.getContadorT()) + " = " + myVarOld.getPosition()  +";\n"
            temporalTPos = c3dObj.getContadorT()
            c3dObj.addContadorT()
            c3dObj.addNumVariable()
            C3D += "    t" + str(c3dObj.getContadorT()) + " = H;\n"
            temporalHEAP = c3dObj.getContadorT()
            c3dObj.addContadorT()

            for valor in self.listaVals:
                tamanio0 += 1
                if isinstance(valor, Primitivo):
                    resultadoC3D = valor.getC3D(c3dObj)
                    if valor.type != TIPO_DATO.CADENA:
                        for value in resultadoC3D:
                            C3D += "    heap[int(H)] = " + str(value) + ";\n"
                            C3D += "    H = H + 1;\n"
                        self.type = TIPO_DATO.DECIMAL
                    else:
                        C3D += resultadoC3D
                        C3D += "    heap[int(H)] = 32;\n"
                        C3D += "    H = H + 1;\n"
                        self.type = TIPO_DATO.CADENA
                else:
                    if not isinstance(valor, list):
                        resultadoC3D = valor.getC3D(c3dObj)
                        C3D += resultadoC3D[0]
                        C3D += "    heap[int(H)] = t" + str(resultadoC3D[1]) + ";\n"
                        C3D += "    H = H + 1;\n"
                    else:
                        listaN = self.recorrerC3D(valor, c3dObj, secondT, dimension)
                        C3D += listaN[0]
                        secondT.append(listaN[1])
                        secondT = secondT[::-1]
            secondT.append({0:tamanio0})
            tamanios = secondT[::-1]
            C3D += "    heap[int(H)] = -1;\n"
            C3D += "    H = H + 1;\n"
            C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(temporalHEAP) + ";\n"
            myNewVariable = VariableC3D(self.identificador, myVarOld.getPosition(), TipoVar.APUNTADOR, self.type, TipoVariable.LISTA, self.line, self.column)
            
            myNewVariable.setTam(tamanios)
        
        if myNewVariable != None:
            c3dObj.addVariable(myNewVariable.getName(), myNewVariable)
        return C3D

    def recorrerC3D(self, listaR, c3dObj, listaT, dimension):
        C3D = ""
        tamanio = 0
        dimension += 1
        listaT1 = []
        for valor in listaR:
            tamanio += 1
            if isinstance(valor, Primitivo):
                resultadoC3D = valor.getC3D(c3dObj)
                if valor.type != TIPO_DATO.CADENA:
                    for value in resultadoC3D:
                        C3D += "    heap[int(H)] = " + str(value) + ";\n"
                        C3D += "    H = H + 1;\n"
                    self.type = TIPO_DATO.DECIMAL
                else:
                    C3D += resultadoC3D
                    C3D += "    heap[int(H)] = 32;\n"
                    C3D += "    H = H + 1;\n"
                    self.type = TIPO_DATO.CADENA
            else:
                if not isinstance(valor, list):
                    resultadoC3D = valor.getC3D(c3dObj)
                    C3D += resultadoC3D[0]
                    C3D += "    heap[int(H)] = t" + str(resultadoC3D[1]) + ";\n"
                    C3D += "    H = H + 1;\n"
                else:
                    resultado = self.recorrerC3D(valor, c3dObj, listaT, dimension)
                    C3D += resultado[0]
                    listaT1.append(resultado[1])
        listaT2 = {dimension: tamanio}
        listaT1.append(listaT2)
        listaT1 =listaT1[::-1]
        return [C3D, listaT1]
        
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