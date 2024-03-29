from Instrucciones.Return import Return
from Instrucciones.AsignacionVar import Asignacion
from Instrucciones.GlobalVar import Global
from Instrucciones.Continue import Continue
from Instrucciones.Break import Break
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Excepciones.Excepcion import Excepcion
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from tablaSimbolos.Tipo import TIPO_DATO
from tablaSimbolos.Tabla import Tabla

class If(AST):
    def __init__(self, type, line, column, condition, instructionIF, instructionsELSE, instructionselseIf):
        super().__init__(type, line, column)
        self.condicion = condition
        self.instruccionIf = instructionIF
        self.instruccionesElse = instructionsELSE
        self.instruccionesElseIf = instructionselseIf

    def getNode(self):
        node = nodeAST("IF")
        node.addChild("if")
        nodeExp = nodeAST("EXPRESION")
        nodeExp.addChildrenNode(self.condicion.getNode())
        node.addChildrenNode(nodeExp)
        nodeInstrucion = nodeAST("INSTRUCCIONES")
        for instruccion in self.instruccionIf:
            if isinstance(instruccion, Excepcion): continue
            nodeInstrucion.addChildrenNode(instruccion.getNode())
        node.addChildrenNode(nodeInstrucion)

        if self.instruccionesElse != None:
            nodeElse = nodeAST("ELSE")
            nodeElse.addChild("else")
            nodeInstElse = nodeAST("INSTRUCCIONES")
            for instrucion in self.instruccionesElse:
                if isinstance(instrucion, Excepcion): continue
                nodeInstElse.addChildrenNode(instrucion.getNode())
            nodeElse.addChildrenNode(nodeInstElse)
            node.addChildrenNode(nodeElse)

        if self.instruccionesElseIf != None:
            nodeElseif = nodeAST("ELSEIF")
            nodeElseif.addChild("else")
            nodeElseif.addChildrenNode(self.instruccionesElseIf.getNode())
            node.addChildrenNode(nodeElseif)
        return node

    def interpretar(self, table, tree, contexto):
        myCondition = self.condicion.interpretar(table, tree)
        if isinstance(myCondition, Excepcion): return myCondition
        if self.condicion.type != TIPO_DATO.BOOLEANO:
            return Excepcion("Semantico", "Se esperaba una expresion booleana", self.line, self.condicion)

        if(myCondition):
            newTable = Tabla(table)
            globalTable = None
            for insIf in self.instruccionIf:
                if isinstance(insIf, Excepcion):
                    tree.updateConsole(insIf.imprimir())
                    continue
                if isinstance(insIf, Return):
                    return insIf
                instruccion = None
                if isinstance(insIf, If):
                    instruccion = insIf.interpretar(newTable, tree, contexto)
                elif isinstance(insIf, Global):
                    instruccion = insIf.interpretar(newTable, tree)
                    globalTable = instruccion
                else:
                    if globalTable != None:
                        instruccion = insIf.interpretar(globalTable, tree)
                    else:
                        instruccion = insIf.interpretar(newTable, tree)
                if isinstance(instruccion, Excepcion): 
                    tree.updateConsole(instruccion.imprimir())
                if isinstance(instruccion, Return):
                    return instruccion
                if contexto != None:
                    if isinstance(instruccion, Break): return instruccion
                    if isinstance(instruccion, Continue): return instruccion
                else:
                    if isinstance(instruccion, Break): return Excepcion("Semantico", "Break se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
                    if isinstance(instruccion, Continue): return Excepcion("Semantico", "Continue se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
        else:
            if self.instruccionesElseIf != None:
                instruccion = self.instruccionesElseIf.interpretar(table, tree, contexto)
                if isinstance(instruccion, Excepcion): return instruccion
                if isinstance(instruccion, Return):
                    return instruccion
                if contexto != None:
                    if isinstance(instruccion, Break): return instruccion
                    if isinstance(instruccion, Continue): return instruccion
                else:
                    if isinstance(instruccion, Break): return Excepcion("Semantico", "Break se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
                    if isinstance(instruccion, Continue): return Excepcion("Semantico", "Continue se encuentra fuera de un ciclo", instruccion.line, instruccion.column)
            elif self.instruccionesElse != None:
                newTable = Tabla(table)
                globalTable = None
                for insElse in self.instruccionesElse:
                    if isinstance(insElse, Excepcion):
                        tree.updateConsole(insElse.imprimir())
                        continue
                    if isinstance(insElse, Return):
                        return insElse

                    instr = None
                    if isinstance(insElse, If):
                        instr = insElse.interpretar(newTable, tree, contexto)
                    elif isinstance(insElse, Global):
                        instr = insElse.interpretar(newTable, tree)
                        globalTable = instr
                    else:
                        if globalTable != None:
                            instr = insElse.interpretar(globalTable, tree)
                        else:
                            instr = insElse.interpretar(newTable, tree)
                    if isinstance(instr, Excepcion): tree.updateConsole(instr.imprimir())
                    if isinstance(instr, Return):
                        return instr
                    if contexto != None:
                        if isinstance(instr, Break): return instr
                        if isinstance(instr, Continue): return instr
                    else:
                        if isinstance(instr, Break): return Excepcion("Semantico", "Break se encuentra fuera de un ciclo", instr.line, instr.column)
                        if isinstance(instr, Continue): return Excepcion("Semantico", "Continue se encuentra fuera de un ciclo", instr.line, instr.column)
        return None

    def getC3D(self, c3dObj, finalL, inicioL):
        C3D = ""
        resultadoCondicion = self.condicion.getC3D(c3dObj)
        # [C3D, LV, LF]
        isReturn = False
        temporalFR = None
        C3D += resultadoCondicion[0] # IF 
        C3D += "    /* REALIZANDO IF */\n"
        if isinstance(self.condicion, Relacional):
            C3D += "    L" + str(resultadoCondicion[1]) + ":\n"
            for instruccion in self.instruccionIf:
                if isinstance(instruccion, Break):
                    C3D += instruccion.getC3D(c3dObj, finalL)
                elif isinstance(instruccion, Continue):
                    C3D += instruccion.getC3D(c3dObj, inicioL)
                elif isinstance(instruccion, If):
                    C3D += instruccion.getC3D(c3dObj, finalL, inicioL)
                elif isinstance(instruccion, Return):
                    C3D += instruccion.getC3D(c3dObj)
                    isReturn = True
                else:
                    resultado = instruccion.getC3D(c3dObj)
                    if isinstance(resultado, list):
                        C3D += resultado[0]
                    else:
                        C3D += resultado
            C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
            temporalLS = c3dObj.getContadorL()
            c3dObj.addContadorL()
            C3D += "    L" + str(resultadoCondicion[2]) + ":\n"
            if self.instruccionesElseIf != None: # ELSE IF
                C3D += self.instruccionesElseIf.getC3D(c3dObj, finalL, inicioL)
            elif self.instruccionesElse != None: # ELSE
                for insElse in self.instruccionesElse:
                    if isinstance(insElse, Break):
                        C3D += insElse.getC3D(c3dObj, finalL)
                    elif isinstance(insElse, Continue):
                        C3D += insElse.getC3D(c3dObj, inicioL)
                    elif isinstance(insElse, If):
                        C3D += insElse.getC3D(c3dObj, finalL, inicioL)
                    else:
                        resultado = insElse.getC3D(c3dObj)
                        if isinstance(resultado, list):
                            C3D += resultado[0]
                        else:
                            C3D += resultado
            C3D += "    L" + str(temporalLS) + ":\n"
        elif isinstance(self.condicion, Logica):
            for valor in resultadoCondicion[1]:
                C3D += "    L" + str(valor) + ":\n"
            for instruccion in self.instruccionIf:
                if isinstance(instruccion, Break):
                    C3D += instruccion.getC3D(c3dObj, finalL)
                elif isinstance(instruccion, Continue):
                    C3D += instruccion.getC3D(c3dObj, inicioL)
                elif isinstance(instruccion, If):
                    C3D += instruccion.getC3D(c3dObj, finalL, inicioL)
                else:
                    resultado = instruccion.getC3D(c3dObj)
                    if isinstance(resultado, list):
                        C3D += resultado[0]
                    else:
                        C3D += resultado
            C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
            temporalLS = c3dObj.getContadorL()
            c3dObj.addContadorL()
            for valor in resultadoCondicion[2]:
                C3D += "    L" + str(valor) + ":\n"
            if self.instruccionesElseIf != None: # ELSE IF
                C3D += self.instruccionesElseIf.getC3D(c3dObj, finalL, inicioL)
            elif self.instruccionesElse != None: # ELSE
                for insElse in self.instruccionesElse:
                    if isinstance(insElse, Break):
                        C3D += insElse.getC3D(c3dObj, finalL)
                    elif isinstance(insElse, Continue):
                        C3D += insElse.getC3D(c3dObj, inicioL)
                    elif isinstance(insElse, If):
                        C3D += insElse.getC3D(c3dObj, finalL, inicioL)
                    else:
                        resultado = insElse.getC3D(c3dObj)
                        if isinstance(resultado, list):
                            C3D += resultado[0]
                        else:
                            C3D += resultado
            C3D += "    L" + str(temporalLS) + ":\n"
        return C3D