from math import isnan
from Instrucciones.Return import Return
from Instrucciones.If import If
from Instrucciones.Continue import Continue
from Instrucciones.Break import Break
from Expresiones.Primitivo import Primitivo
from Instrucciones.AsignacionVar import Asignacion
from Expresiones.Identificador import Identificador
from C3D.variableC3D import TipoVar
from C3D.variableC3D import VariableC3D
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tabla import Tabla
from C3D.variableC3D import TipoVariable

class For(AST):

    def __init__(self, type, line, column, varName, objeto1, objeto2, instructions):
        super().__init__(type, line, column)
        self.nombre = varName
        self.objeto1 = objeto1
        self.objeto2 = objeto2
        self.instrucciones = instructions

    def getNode(self):
        node = nodeAST("FOR")
        node.addChild("for")
        node.addChild(str(self.nombre))
        node.addChild("in")
        if isinstance(self.objeto1, list):
            for pedazo in self.objeto1:
                node.addChildrenNode(pedazo.getNode())
                if pedazo != self.objeto1[-1]:
                    node.addChild(", ")
        else:
            if self.objeto1.type == TIPO_DATO.CADENA:
                node.addChildrenNode(self.objeto1.getNode())
            elif self.objeto1.type == TIPO_DATO.LISTA:
                node.addChildrenNode(self.objeto1.getNode())
            elif self.objeto1.type == TIPO_DATO.ENTERO:
                if self.objeto2 != None:
                    if self.objeto2.type == TIPO_DATO.ENTERO:
                        node.addChildrenNode(self.objeto1.getNode())
                        node.addChild(":")
                        node.addChildrenNode(self.objeto2.getNode())
        nodeIns = nodeAST("INSTRUCCIONES")
        for instruccion in self.instrucciones:
            if isinstance(instruccion, Excepcion): continue
            nodeIns.addChildrenNode(instruccion.getNode())
        node.addChildrenNode(nodeIns)
        node.addChild("end;")            
        return node
    
    def interpretar(self, table, tree):
        newTable = Tabla(table)
        if self.type == TIPO_DATO.CADENA:
            if isinstance(self.objeto1, list):
                for valor in self.objeto1:
                    myVal = None
                    newVal = None
                    if isinstance(valor, list):
                        myVal = self.recorrerList(valor, table, tree)
                        if isinstance(myVal, Primitivo): myVal = myVal.interpretar(table, tree)
                        newVal = Primitivo(valor[0].type, self.line, self.column, myVal)
                    else:
                        myVal = valor.interpretar(table, tree)
                        if isinstance(myVal, Primitivo): myVal = myVal.interpretar(table, tree)
                        newVal = Primitivo(valor.type, self.line, self.column, myVal)
                    variable = Asignacion(self.line, self.column, self.nombre, newVal, newVal.type).interpretar(newTable, tree)
                    if variable != None:
                        return variable
                    for instruccion in self.instrucciones:
                        if isinstance(instruccion, Excepcion):
                            tree.updateConsole(instruccion.imprimir())
                            continue
                        if isinstance(instruccion, Return):
                            return instruccion
                        result = None
                        if isinstance(instruccion, If):
                            result = instruccion.interpretar(newTable, tree, 'For')
                        else:
                            result = instruccion.interpretar(newTable, tree)
                        if isinstance(result, Excepcion):
                            tree.updateConsole(result.imprimir())
                        if isinstance(result, Return):
                            return result
                        if isinstance(result, Break):
                            return None
                        if isinstance(result, Continue):
                            break
            else:
                cad = self.objeto1.interpretar(table, tree)
                if self.objeto1.type == TIPO_DATO.LISTA:
                    for string in cad.value:
                        myVal = None
                        newVal = None
                        if isinstance(string, list):
                            myVal = self.recorrerList(string, table, tree)
                            if isinstance(myVal, Primitivo): myVal = myVal.interpretar(table, tree)
                            newVal = Primitivo(string[0].type, self.line, self.column, myVal)
                        else:
                            myVal = string.interpretar(table, tree)
                            if isinstance(myVal, Primitivo): myVal = myVal.interpretar(table, tree)
                            newVal = Primitivo(string.type, self.line, self.column, myVal)
                        variable = Asignacion(self.line, self.column, self.nombre, newVal, newVal.type).interpretar(newTable, tree)
                        if variable != None:
                            return variable
                        for instruccion in self.instrucciones:
                            if isinstance(instruccion, Excepcion):
                                tree.updateConsole(instruccion.imprimir())
                                continue
                            if isinstance(instruccion, Return):
                                return instruccion
                            result = None
                            if isinstance(instruccion, If):
                                result = instruccion.interpretar(newTable, tree, 'For')
                            else:
                                result = instruccion.interpretar(newTable, tree)
                            if isinstance(result, Excepcion):
                                tree.updateConsole(result.imprimir())
                            if isinstance(result, Return):
                                return result
                            if isinstance(result, Break):
                                return None
                            if isinstance(result, Continue):
                                break
                else:
                    if isinstance(cad, Primitivo): cad = cad.interpretar(table, tree)
                    myCadena = str(cad)
                    for cadena in myCadena:
                        valor = Primitivo(TIPO_DATO.CARACTER, self.line, self.column, cadena)
                        variable = Asignacion(self.line, self.column, self.nombre, valor, TIPO_DATO.CARACTER).interpretar(newTable, tree)
                        if variable != None:
                            return variable
                        for instruccion in self.instrucciones:
                            if isinstance(instruccion, Excepcion):
                                tree.updateConsole(instruccion.imprimir())
                                continue
                            if isinstance(instruccion, Return):
                                return instruccion
                            result = None
                            if isinstance(instruccion, If):
                                result = instruccion.interpretar(newTable, tree, 'For')
                            else:
                                result = instruccion.interpretar(newTable, tree)
                            if isinstance(result, Excepcion):
                                tree.updateConsole(result.imprimir())
                            if isinstance(result, Return):
                                return result
                            if isinstance(result, Break):
                                return None
                            if isinstance(result, Continue):
                                break
        elif self.type == TIPO_DATO.ENTERO:
            if self.objeto2 != None:
                val1 = self.objeto1.interpretar(table, tree)
                if isinstance(val1, Excepcion): return val1
                if isinstance(val1, Primitivo): val1 = val1.interpretar(table, tree)
                val2 = self.objeto2.interpretar(table, tree)
                if isinstance(val2, Excepcion): return val2
                if isinstance(val2, Primitivo):                    
                    if val2.type != TIPO_DATO.ENTERO: 
                        return Excepcion("Semantico", "El iterable no es valida", self.line, self.column)
                    val2 = val2.interpretar(table, tree)
                valor1 = int(val1)
                valor2 = int(val2)
                for numero in range(valor1, valor2 + 1):
                    valor = Primitivo(TIPO_DATO.ENTERO, self.line, self.column, numero)
                    variable = Asignacion(self.line, self.column, self.nombre, valor, TIPO_DATO.ENTERO).interpretar(newTable, tree)
                    if variable != None:
                        return variable
                    for instruccion in self.instrucciones:
                        if isinstance(instruccion, Excepcion):
                            tree.updateConsole(instruccion.imprimir())
                            continue
                        if isinstance(instruccion, Return):
                            return instruccion
                        result = None
                        if isinstance(instruccion, If):
                            result = instruccion.interpretar(newTable, tree, 'For')
                        else:
                            result = instruccion.interpretar(newTable, tree)
                        if isinstance(result, Excepcion):
                            tree.updateConsole(result.imprimir())
                        if isinstance(result, Return):
                            return result
                        if isinstance(result, Break):
                            return None
                        if isinstance(result, Continue):
                            break
        
        else:
            return Excepcion("Semantico", "El iterable no es valido", self.line, self.column)
        return None

    def recorrerList(self, lista, table, tree):
        texto = "["
        for valor in lista:
            if isinstance(valor, list):
                    texto += self.recorrerList(valor, table, tree)
            else:
                content = valor.interpretar(table, tree)
                if valor.type == TIPO_DATO.CADENA:
                    texto += "\""
                elif valor.type == TIPO_DATO.CARACTER:
                    texto += "'"
                
                if isinstance(content, Primitivo):
                    content = content.interpretar(table, tree)
                texto += str(content)

                if valor.type == TIPO_DATO.CADENA:
                    texto += "\""
                elif valor.type == TIPO_DATO.CARACTER:
                    texto += "'"
            if valor != lista[-1]:
                texto += ", "
        texto += "]"
        return texto

    def getC3D(self, c3dObj):
        C3D = "    /* EJECUCION FOR */\n"
        codeInt = ""
        if self.type == TIPO_DATO.CADENA:
            if isinstance(self.objeto1, Primitivo):
                cadena = self.objeto1.getValue()
                for valor in cadena:
                    newValue = Primitivo(self.type, self.line, self.column, valor)
                    newVar = Asignacion(self.line, self.column, self.nombre, newValue).getC3D(c3dObj)
                    codeInt += newVar
                    for instruccion in self.instrucciones:
                        if isinstance(instruccion, Break):
                            codeInt += instruccion.getC3D(c3dObj, None)
                        elif isinstance(instruccion, Continue):
                            codeInt += instruccion.getC3D(c3dObj, None)
                        elif isinstance(instruccion, If):
                            codeInt += instruccion.getC3D(c3dObj, None, None)
                        else:
                            codeInt += instruccion.getC3D(c3dObj)
            elif isinstance(self.objeto1, Identificador):
                resultadoC3D = self.objeto1.getC3D(c3dObj)
                codeInt += resultadoC3D[0]
                codeInt2 = "    t" + str(c3dObj.getContadorT()) + " = heap[int(t" + str(resultadoC3D[1]) + ")];\n"
                temporalPOSHEAP = c3dObj.getContadorT()
                c3dObj.addContadorT()
                codeInt2 += "    /* ASIGNANDO VARIABLE */\n"
                codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                temporalPos = c3dObj.getContadorT()
                c3dObj.addContadorT()
                c3dObj.addNumVariable()
                codeInt2 += "    if t" + str(temporalPOSHEAP) + " == -1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                temporalS = c3dObj.getContadorL()
                c3dObj.addContadorL()
                codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = H;\n"
                temporalAsi = c3dObj.getContadorT()
                c3dObj.addContadorT()
                codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = heap[int(t" + str(resultadoC3D[1]) +")];\n"
                temporalHeap = c3dObj.getContadorT()
                c3dObj.addContadorT()
                codeInt2 += "    heap[int(H)] = t" + str(temporalHeap) +";\n"
                c3dObj.addContadorT()
                
                codeInt2 += "    H = H + 1;\n"
                c3dObj.addContadorT()
                codeInt2 += "    t" + str(resultadoC3D[1]) + " = t" + str(resultadoC3D[1]) + " + 1;\n"
                codeInt2 += "    heap[int(H)] = -1;\n"

                codeInt2 += "    stack[int(t" + str(temporalPos) + ")] = t" + str(temporalAsi) + ";\n"
                myNewVariable = VariableC3D(self.nombre, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.APUNTADOR, self.objeto1.type, TipoVariable.VARIABLE)
                c3dObj.addVariable(myNewVariable.getName(), myNewVariable)
                for instruccion in self.instrucciones:
                    if isinstance(instruccion, Break):
                        codeInt2 += instruccion.getC3D(c3dObj, None)
                    elif isinstance(instruccion, Continue):
                        codeInt2 += instruccion.getC3D(c3dObj, None)
                    elif isinstance(instruccion, If):
                        codeInt2 += instruccion.getC3D(c3dObj, None)
                    else:
                        codeInt2 += instruccion.getC3D(c3dObj)
                codeInt2 += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                temporalLini =c3dObj.getContadorL()
                c3dObj.addContadorL()

                codeInt += "    L" + str(temporalLini) + ":\n"
                codeInt += codeInt2
                codeInt += "    L" + str(temporalS) + ":\n"
        elif self.type == TIPO_DATO.ENTERO:
            if isinstance(self.objeto1, Primitivo):
                if isinstance(self.objeto2, Primitivo):
                    valorIni = int(self.objeto1.getValue())
                    valorFin = int(self.objeto2.getValue())
                    for numero in range(valorIni, valorFin + 1):
                        newValue = Primitivo(self.type, self.line, self.column, numero)
                        newVar = Asignacion(self.line, self.column, self.nombre, newValue).getC3D(c3dObj)
                        codeInt += newVar
                        for instruccion in self.instrucciones:
                            if isinstance(instruccion, Break):
                                codeInt += instruccion.getC3D(c3dObj, None)
                            elif isinstance(instruccion, Continue):
                                codeInt += instruccion.getC3D(c3dObj, None)
                            elif isinstance(instruccion, If):
                                codeInt += instruccion.getC3D(c3dObj, None)
                            else:
                                codeInt += instruccion.getC3D(c3dObj)
                else:
                    valorIni = self.objeto1.getC3D(c3dObj)
                    valorFin = self.objeto2.getC3D(c3dObj)
                    codeInt += valorFin[0]
                    codeInt += "    /* ASIGNANDO VARIABLE */\n"
                    codeInt += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                    temporalPos = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    c3dObj.addNumVariable()
                    for valor in valorIni: # ASIGNANDO VALOR INICIO
                        codeInt += "    t" + str(c3dObj.getContadorT()) + " = " + str(valor) + ";\n"
                        temporalVal = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        codeInt += "    stack[int(t" + str(temporalPos) + ")] = t" + str(temporalVal) + ";\n"
                    myNewVariable = VariableC3D(self.nombre, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.VALOR, self.objeto1.type, TipoVariable.VARIABLE)
                    c3dObj.addVariable(myNewVariable.getName(), myNewVariable)
                    codeInt2 = "    /* VALIDANDO FOR */\n"
                    myOldVariable = c3dObj.getVariable(self.nombre)
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux1 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalAux1) + ")];\n"
                    temporalAux2 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    if t" + str(temporalAux2) + " > t" + str(valorFin[1]) + " { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                    temporalLSal = c3dObj.getContadorL()
                    c3dObj.addContadorL()
                    for instruccion in self.instrucciones:
                        if isinstance(instruccion, Break):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        elif isinstance(instruccion, Continue):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        elif isinstance(instruccion, If):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        else:
                            codeInt2 += instruccion.getC3D(c3dObj)
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux3 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux4 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalAux4) + ")];\n"
                    temporalAux5 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux5) + " + 1;\n"
                    temporalAux6 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    stack[int(t" + str(temporalAux3) + ")] = t" + str(temporalAux6) + ";\n"
                    codeInt2 += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                    temporalLReg = c3dObj.getContadorL()
                    c3dObj.addContadorL()

                    codeInt += "    L" + str(temporalLReg) + ":\n"
                    codeInt += codeInt2
                    codeInt += "    L" + str(temporalLSal) + ":\n"
            else:
                if isinstance(self.objeto2, Primitivo):
                    valorIni = self.objeto1.getC3D(c3dObj)
                    valorFin = self.objeto2.getC3D(c3dObj)
                    codeInt += valorIni[0]
                    codeInt += "    /* ASIGNANDO VARIABLE */\n"
                    codeInt += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                    temporalPos = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    c3dObj.addNumVariable()
                    codeInt += "    t" + str(c3dObj.getContadorT()) + " = t" + str(valorIni[1]) + ";\n"
                    temporalVal = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt += "    stack[int(t" + str(temporalPos) + ")] = t" + str(temporalVal) + ";\n"
                    myNewVariable = VariableC3D(self.nombre, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.VALOR, self.objeto1.type, TipoVariable.VARIABLE)
                    c3dObj.addVariable(myNewVariable.getName(), myNewVariable)
                    
                    
                    codeInt2 = "    /* VALIDANDO FOR */\n"
                    myOldVariable = c3dObj.getVariable(self.nombre)
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux1 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalAux1) + ")];\n"
                    temporalAux2 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    for valor in valorFin:
                        codeInt2 += "    if t" + str(temporalAux2) + " > " + str(valor) + " { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                    temporalLSal = c3dObj.getContadorL()
                    c3dObj.addContadorL()
                    for instruccion in self.instrucciones:
                        if isinstance(instruccion, Break):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        elif isinstance(instruccion, Continue):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        elif isinstance(instruccion, If):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        else:
                            codeInt2 += instruccion.getC3D(c3dObj)
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux3 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux4 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalAux4) + ")];\n"
                    temporalAux5 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux5) + " + 1;\n"
                    temporalAux6 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    stack[int(t" + str(temporalAux3) + ")] = t" + str(temporalAux6) + ";\n"
                    codeInt2 += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                    temporalLReg = c3dObj.getContadorL()
                    c3dObj.addContadorL()

                    codeInt += "    L" + str(temporalLReg) + ":\n"
                    codeInt += codeInt2
                    codeInt += "    L" + str(temporalLSal) + ":\n"
                else:
                    valorIni = self.objeto1.getC3D(c3dObj)
                    valorFin = self.objeto2.getC3D(c3dObj)
                    codeInt += valorIni[0]
                    codeInt += valorFin[0]
                    codeInt += "    /* ASIGNANDO VARIABLE */\n"
                    codeInt += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                    temporalPos = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    c3dObj.addNumVariable()
                    codeInt += "    t" + str(c3dObj.getContadorT()) + " = t" + str(valorIni[1]) + ";\n"
                    temporalVal = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt += "    stack[int(t" + str(temporalPos) + ")] = t" + str(temporalVal) + ";\n"
                    myNewVariable = VariableC3D(self.nombre, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.VALOR, self.objeto1.type, TipoVariable.VARIABLE)
                    c3dObj.addVariable(myNewVariable.getName(), myNewVariable)
                    
                    
                    codeInt2 = "    /* VALIDANDO FOR */\n"
                    myOldVariable = c3dObj.getVariable(self.nombre)
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux1 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalAux1) + ")];\n"
                    temporalAux2 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    if t" + str(temporalAux2) + " > t" + str(valorFin[1]) + " { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                    temporalLSal = c3dObj.getContadorL()
                    c3dObj.addContadorL()
                    for instruccion in self.instrucciones:
                        if isinstance(instruccion, Break):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        elif isinstance(instruccion, Continue):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        elif isinstance(instruccion, If):
                            codeInt2 += instruccion.getC3D(c3dObj, None)
                        else:
                            codeInt2 += instruccion.getC3D(c3dObj)
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux3 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = " + str(myOldVariable.getPosition()) + ";\n"
                    temporalAux4 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalAux4) + ")];\n"
                    temporalAux5 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux5) + " + 1;\n"
                    temporalAux6 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    codeInt2 += "    stack[int(t" + str(temporalAux3) + ")] = t" + str(temporalAux6) + ";\n"
                    codeInt2 += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                    temporalLReg = c3dObj.getContadorL()
                    c3dObj.addContadorL()

                    codeInt += "    L" + str(temporalLReg) + ":\n"
                    codeInt += codeInt2
                    codeInt += "    L" + str(temporalLSal) + ":\n"

        C3D += codeInt
        return C3D