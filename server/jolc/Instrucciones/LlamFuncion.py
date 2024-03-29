from Instrucciones.AsignStructN import StructN
from Expresiones.Atributo import Atributo
from Expresiones.Primitivo import Primitivo
from Instrucciones.AsignacionVar import Asignacion
from Instrucciones.Return import Return
from Instrucciones.If import If
from Expresiones.IdLista import IdLista
from tablaSimbolos.Tabla import Tabla
from Instrucciones.Continue import Continue
from Instrucciones.Break import Break
from Excepciones.Excepcion import Excepcion
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO
from tablaSimbolos.Simbolo import Simbolo

class LlamadaFuncion(AST):

    def __init__(self, line, column, identifier, params):
        super().__init__(TIPO_DATO.FUNCION, line, column)
        self.identificador = identifier
        self.parametros = params

    def getNode(self):
        node = None
        node = nodeAST("LLAMADA FUNCION/STRUCT")
        node.addChild(self.identificador)
        node.addChild("(")
        if self.parametros != None:
            nodeParams = nodeAST("PARAMETROS")
            for parametro in self.parametros:
                nodeParams.addChildrenNode(parametro.getNode())
            node.addChildrenNode(nodeParams)
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        listFunctions = table.getVariable(self.identificador)
        if listFunctions != None and listFunctions.type == TIPO_DATO.FUNCION:
            myFunction = listFunctions.getValor()
            self.type = TIPO_DATO.FUNCION
            newTable = Tabla(table)
            if myFunction.parametros == None:
                if self.parametros != None:
                    return Excepcion("Semantico", "La función no require parametros", self.line, self.column)
                else:
                    instrucciones = myFunction.instrucciones
                    for instFunc in instrucciones:
                        if isinstance(instFunc, Excepcion):
                            tree.updateConsole(instFunc.imprimir())
                            continue
                        instruccion = None
                        if isinstance(instFunc, If):
                            instruccion = instFunc.interpretar(newTable, tree, None)
                        elif isinstance(instFunc, Return):
                            return instFunc.interpretar(newTable, tree)
                        else:
                            instruccion = instFunc.interpretar(newTable, tree)
                        if isinstance(instruccion, Excepcion): tree.updateConsole(instruccion.imprimir())
                        if isinstance(instruccion, Return):
                            return instruccion.interpretar(table, tree)
                        if isinstance(instruccion, Break): return Excepcion("Semantico", "Break se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
                        if isinstance(instruccion, Continue): return Excepcion("Semantico", "Continue se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
            else:
                if self.parametros == None:
                    return Excepcion("Semantico", "La función require parametros", self.line, self.column)
                else:
                    for i in range(len(self.parametros)):
                        valor = self.parametros[i]
                        variable = myFunction.parametros[i]

                        value = valor.interpretar(table, tree)
                        simbolo = None
                        if isinstance(value, Excepcion): return value

                        if isinstance(value, Primitivo):
                            self.type = value.type
                            simbolo = Simbolo(self.type, variable.identificador, self.line, self.column, value)
                        else:
                            self.type = valor.type
                            valor = Primitivo(valor.type, self.line, self.column, value)
                            simbolo = Simbolo(self.type, variable.identificador, self.line, self.column, valor)
                        
                        newTable.setVariable(simbolo)
                    instrucciones = myFunction.instrucciones
                    for instFunc in instrucciones:
                        if isinstance(instFunc, Excepcion):
                            tree.updateConsole(instFunc.imprimir())
                            continue
                        instruccion = None
                        if isinstance(instFunc, If):
                            instruccion = instFunc.interpretar(newTable, tree, None)
                        elif isinstance(instFunc, Return):
                            return instFunc.interpretar(newTable, tree)
                        else:
                            instruccion = instFunc.interpretar(newTable, tree)
                        if isinstance(instruccion, Excepcion): tree.updateConsole(instruccion.imprimir())
                        if isinstance(instruccion, Return):
                            return instruccion.interpretar(newTable, tree)
                        if isinstance(instruccion, Break): return Excepcion("Semantico", "Break se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
                        if isinstance(instruccion, Continue): return Excepcion("Semantico", "Continue se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
        else:
            myStruct = table.getVariable(self.identificador)
            if myStruct != None and (myStruct.type == TIPO_DATO.STRUCTN or myStruct.type == TIPO_DATO.STRUCTM):
                self.type = myStruct.type
                tamSParams = len(myStruct.value)
                tamParams = len(self.parametros)
                if tamSParams == tamParams:
                    nuevosParams = []
                    for numero in range(tamParams):
                        vParam = myStruct.value[numero]
                        nParam = self.parametros[numero]
                        nAtributo = None
                        if vParam.type == None:
                            if isinstance(nParam, Primitivo):
                                nAtributo = Atributo(self.line, self.column, vParam.identificador, nParam, vParam.type)
                            else:
                                oParam = nParam.interpretar(table, tree)
                                nAtributo = Atributo(self.line, self.column, vParam.identificador, oParam, vParam.type)
                        else:
                            if isinstance(nParam, Primitivo):
                                tipoP = vParam.type
                                tipoA = nParam.type
                                if not isinstance(tipoP, str):
                                    if tipoP == tipoA:
                                        nAtributo = Atributo(self.line, self.column, vParam.identificador, nParam, vParam.type)
                                    else:
                                        return Excepcion("Semantico", "Los tipos deben de ser los mismos", self.line, self.column)
                                else:
                                    tipoStruct = table.getVariable(tipoP)
                                    if tipoStruct != None:
                                        if tipoStruct == nParam.identificador:
                                            nAtributo = Atributo(self.line, self.column, vParam.identificador, nParam, vParam.type)
                                        else:
                                            return Excepcion("Semantico", "Los tipos deben de ser los mismos", self.line, self.column)
                                    else:
                                        return Excepcion("Semantico", "El tipo no es valido", self.line, self.column)
                            else:
                                otherParam = nParam.interpretar(table, tree)
                                tipoP = vParam.type
                                tipoA = nParam.type
                                if not isinstance(tipoP, str):
                                    if tipoP == tipoA:
                                        nAtributo = Atributo(self.line, self.column, vParam.identificador, otherParam, vParam.type)
                                    else:
                                        return Excepcion("Semantico", "Los tipos deben de ser los mismos", self.line, self.column)
                                else:
                                    tipoStruct = table.getVariable(tipoP)
                                    if tipoStruct != None:
                                        tipoStruct = tipoStruct.getId()
                                        if isinstance(nParam, LlamadaFuncion):
                                            if tipoStruct == nParam.identificador:
                                                nAtributo = Atributo(self.line, self.column, vParam.identificador, otherParam, vParam.type)
                                            else:
                                                return Excepcion("Semantico", "Los tipos deben de ser los mismos", self.line, self.column)
                                        else:
                                            if tipoStruct == tipoA:
                                                nAtributo = Atributo(self.line, self.column, vParam.identificador, otherParam, vParam.type)
                                            else:
                                                return Excepcion("Semantico", "Los tipos deben de ser los mismos", self.line, self.column)
                                    else:
                                        return Excepcion("Semantico", "El tipo no es valido", self.line, self.column)
                        nuevosParams.append(nAtributo)
                    simboloG = Simbolo(myStruct.type, myStruct.id, self.line, self.column, nuevosParams)
                    return simboloG
                else:
                    return Excepcion("Semantico", "Hacen falta o hay atributos de mas", self.line, self.column)
            
            return Excepcion("Semantico", "La función o struct " + self.identificador +  " no ha sido creada", self.line, self.column)
        return None
    
    def recorrerSimbolo(self, valor, table, tree):
        if isinstance(valor, Simbolo):
            return valor
        else:
            valor = valor.interpretar(table, tree)
            valor = self.recorrerSimbolo(valor, table, tree)

    def getC3D(self, c3dObj):
        C3D1 = "    /* LLAMADA FUNCION */\n"
        C3D2 = ""
        myFuncion = c3dObj.getFunction(self.identificador)
        numVars = len(self.parametros)
        isReturn = False
        for instruccion in myFuncion.value.instrucciones:
            if isinstance(instruccion, Return):
                isReturn = True
            if isinstance(instruccion, Asignacion):
                numVars += 1
        isList = False
        temporalF = None
        if myFuncion != None:
            if self.parametros is not None:
                C3D1 += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                temporal1 = c3dObj.getContadorT()
                c3dObj.addContadorT()
                for i in range(len(self.parametros)):
                    parametro = self.parametros[i]
                    C3D1 += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporal1) + " + " + str(i) + ";\n"
                    temporal2 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    if isinstance(parametro, Primitivo):
                        valor = parametro.interpretar(None, None)
                        C3D1 += "    stack[int(t" + str(temporal2) + ")] = " + str(valor) + ";\n"
                    else:
                        resultado = parametro.getC3D(c3dObj)
                        C3D1 += resultado[0]
                        contadorR = resultado[1]
                        if isinstance(parametro, IdLista):
                            for etiqueta in resultado[2]:
                                C3D2 += "    L" + str(etiqueta) + ":\n"
                            C3D1 += "    t" + str(c3dObj.getContadorT()) + " = heap[int(t" + str(contadorR) + ")];\n"
                            contadorR = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                        C3D1 += "    stack[int(t" + str(temporal2) + ")] = t" + str(contadorR) + ";\n"
            C3D1 += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
            C3D1 += "    " + str(self.identificador) + "();\n"
            if isReturn:
                C3D1 += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(numVars) + ";\n"
                temporalT1 = c3dObj.getContadorT()
                c3dObj.addContadorT()
                C3D1 += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT1) + ")];\n"
                temporalF = c3dObj.getContadorT()
                c3dObj.addContadorT()
            C3D1 += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
            C3D1 += C3D2
            C3D1 += "    /* FIN LLAMADA FUNCION */\n"
        return [C3D1, temporalF]