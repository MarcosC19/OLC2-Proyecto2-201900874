from tablaSimbolos.Tipo import TIPO_DATO
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import OPERADOR_LOGICO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class Logica(AST):
    def __init__(self, type, line, column, operator, operating1, operating2 = None):
        super().__init__(type, line, column)
        self.operator = operator
        self.operating1 = operating1
        self.operating2 = operating2
    
    def getNode(self):
        node = nodeAST("LOGICA")
        if(self.operating2 == None):
            node.addChild("!")
            node.addChildrenNode(self.operating1.getNode())
        else:
            node.addChildrenNode(self.operating1.getNode())
            if self.operator == OPERADOR_LOGICO.AND: node.addChild("&&")
            if self.operator == OPERADOR_LOGICO.OR: node.addChild("||")
            node.addChildrenNode(self.operating2.getNode())
        return node

    def interpretar(self, table, tree):
        izquierdo = None
        derecho = None
        # INTERPRETANDO OPERANDOS
        if self.operating2 == None:
            izquierdo = self.operating1.interpretar(table, tree)
            if isinstance(izquierdo, Excepcion): return izquierdo
            if isinstance(izquierdo, Primitivo):  
                self.operating1.type = izquierdo.type
                izquierdo = izquierdo.interpretar(table, tree)
        else:
            izquierdo = self.operating1.interpretar(table, tree)
            if isinstance(izquierdo, Excepcion): return izquierdo
            if isinstance(izquierdo, Primitivo):  
                self.operating1.type = izquierdo.type
                izquierdo = izquierdo.interpretar(table, tree)
            derecho = self.operating2.interpretar(table, tree)
            if isinstance(derecho, Excepcion): return derecho
            if isinstance(derecho, Primitivo):  
                self.operating2.type = derecho.type
                derecho = derecho.interpretar(table, tree)

        # RETORNANDO VALORES
        # OPERACION AND
        if self.operator == OPERADOR_LOGICO.AND:
            if self.operating1.type == TIPO_DATO.BOOLEANO:
                if self.operating2.type == TIPO_DATO.BOOLEANO:
                    self.type = TIPO_DATO.BOOLEANO
                    return bool(izquierdo) and bool(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es de tipo Bool", self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no es de tipo Bool", self.line, self.column)
        # OPERACION OR
        elif self.operator == OPERADOR_LOGICO.OR:
            if self.operating1.type == TIPO_DATO.BOOLEANO:
                if self.operating2.type == TIPO_DATO.BOOLEANO:
                    self.type = TIPO_DATO.BOOLEANO
                    return bool(izquierdo) or bool(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es de tipo Bool", self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no es de tipo Bool", self.line, self.column)
        # OPERACION NOT
        elif self.operator == OPERADOR_LOGICO.NOT:
            if self.operating1.type == TIPO_DATO.BOOLEANO:
                self.type = TIPO_DATO.BOOLEANO
                return not bool(izquierdo)
            else:
                return Excepcion("Semantico", "Operando 1 no es de tipo Bool", self.line, self.column)
        # CUALQUIER OTRO
        else:
            return Excepcion("Semantico", "Operador no valido", self.line, self.column)

    def getC3D(self, c3dObj):
        C3D = "    /* ANALIZANDO EXPRESION LOGICA */\n"
        LV = []
        LF = []
        # OPERACION AND
        if self.operator == OPERADOR_LOGICO.AND:
            if self.operating1.type == TIPO_DATO.BOOLEANO:
                if self.operating2.type == TIPO_DATO.BOOLEANO:
                    self.type = TIPO_DATO.BOOLEANO
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating1, Primitivo):
                        C3D += resultado1C3D
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        temporalAux1 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += c3dObj.chargeTrue()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        temporalAux1 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 1;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    compareString();\n"
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                        temporalT3 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                        temporalT4 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    if t" + str(temporalT4) + " == 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        C3D += "    L" + str(temporalL0) + ":\n"
                        if isinstance(self.operating2, Primitivo):
                            C3D += resultado2C3D
                            C3D += c3dObj.endString()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            temporalAux2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 0;\n"
                            temporalT2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
                            C3D += c3dObj.chargeTrue()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            temporalAux1 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 1;\n"
                            temporalT2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                            C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            C3D += "    compareString();\n"
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                            temporalT3 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                            temporalT4 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                            C3D += "    if t" + str(temporalT4) + " == 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                            temporalL2 = c3dObj.getContadorL()
                            c3dObj.addContadorL()
                            C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                            temporalL3 = c3dObj.getContadorL()
                            c3dObj.addContadorL()
                            LV.append(temporalL2)
                            LF.append(temporalL1)
                            LF.append(temporalL3)
                        else:
                            C3D += resultado2C3D[0]
                            if isinstance(resultado2C3D[1], list):
                                LV.extend(resultado2C3D[1])
                            else:
                                LV.append(resultado2C3D[1])
                            LF.append(temporalL1)
                            if isinstance(resultado2C3D[2], list):
                                LF.extend(resultado2C3D[2])
                            else:
                                LF.append(resultado2C3D[2])
                    else:
                        C3D += resultado1C3D[0]
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(resultado1C3D[1], list):
                            for valor in resultado1C3D[1]:
                                C3D += "    L" + str(valor) + ":\n"
                        else:
                            C3D += "    L" + str(resultado1C3D[1]) + ":\n"
                        if isinstance(self.operating2, Primitivo):
                            C3D += resultado2C3D
                            C3D += c3dObj.endString()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            temporalAux2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 0;\n"
                            temporalT2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
                            C3D += c3dObj.chargeTrue()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            temporalAux1 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 1;\n"
                            temporalT2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                            C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            C3D += "    compareString();\n"
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                            temporalT3 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                            temporalT4 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                            C3D += "    if t" + str(temporalT4) + " == 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                            temporalL2 = c3dObj.getContadorL()
                            c3dObj.addContadorL()
                            C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                            temporalL3 = c3dObj.getContadorL()
                            c3dObj.addContadorL()
                            LV.append(temporalL2)
                            if isinstance(resultado1C3D[2], list):
                                LF.extend(resultado1C3D[2])
                            else:
                                LF.append(resultado1C3D[2])
                            LF.append(temporalL3)
                        else:
                            C3D += resultado2C3D[0]
                            if isinstance(resultado2C3D[1], list):
                                LV.extend(resultado2C3D[1])
                                if isinstance(resultado1C3D[2], list):
                                    LF.extend(resultado1C3D[2])
                                else:
                                    LF.append(resultado1C3D[2])
                                if isinstance(resultado2C3D[2], list):
                                    LF.extend(resultado2C3D[2])
                                else:
                                    LF.append(resultado2C3D[2])
                            else:
                                LV.append(resultado2C3D[1])
                                if isinstance(resultado1C3D[2], list):
                                    LF.extend(resultado1C3D[2])
                                else:
                                    LF.append(resultado1C3D[2])
                                if isinstance(resultado2C3D[2], list):
                                    LF.extend(resultado2C3D[2])
                                else:
                                    LF.append(resultado2C3D[2])

        # OPERACION OR
        elif self.operator == OPERADOR_LOGICO.OR:
            if self.operating1.type == TIPO_DATO.BOOLEANO:
                if self.operating2.type == TIPO_DATO.BOOLEANO:
                    self.type = TIPO_DATO.BOOLEANO
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating1, Primitivo):
                        C3D += resultado1C3D
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        temporalAux1 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += c3dObj.chargeTrue()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        temporalAux1 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 1;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    compareString();\n"
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                        temporalT3 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                        temporalT4 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    if t" + str(temporalT4) + " == 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        C3D += "    L" + str(temporalL1) + ":\n"
                        if isinstance(self.operating2, Primitivo):
                            C3D += resultado2C3D
                            C3D += c3dObj.endString()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            temporalAux2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 0;\n"
                            temporalT2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
                            C3D += c3dObj.chargeTrue()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            temporalAux1 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 1;\n"
                            temporalT2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                            C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            C3D += "    compareString();\n"
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                            temporalT3 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                            temporalT4 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                            C3D += "    if t" + str(temporalT4) + " == 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                            temporalL2 = c3dObj.getContadorL()
                            c3dObj.addContadorL()
                            C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                            temporalL3 = c3dObj.getContadorL()
                            c3dObj.addContadorL()
                            LV.append(temporalL0)
                            LV.append(temporalL2)
                            LF.append(temporalL3)
                        else:
                            C3D += resultado2C3D[0]
                            LV.append(temporalL0)
                            if isinstance(resultado2C3D[1], list):
                                LV.extend(resultado2C3D[1])
                            else:
                                LV.append(resultado2C3D[1])
                            if isinstance(resultado2C3D[2], list):
                                LF.extend(resultado2C3D[2])
                            else:
                                LF.append(resultado2C3D[2])
                    else:
                        C3D += resultado1C3D[0]
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(resultado1C3D[1], list):
                            for valor in resultado1C3D[2]:
                                C3D += "    L" + str(valor) + ":\n"
                        else:
                            C3D += "    L" + str(resultado1C3D[2]) + ":\n"
                        if isinstance(self.operating2, Primitivo):
                            C3D += resultado2C3D
                            C3D += c3dObj.endString()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            temporalAux2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 0;\n"
                            temporalT2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
                            C3D += c3dObj.chargeTrue()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            temporalAux1 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 1;\n"
                            temporalT2 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                            C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                            C3D += "    compareString();\n"
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                            temporalT3 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                            temporalT4 = c3dObj.getContadorT()
                            c3dObj.addContadorT()
                            C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                            C3D += "    if t" + str(temporalT4) + " == 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                            temporalL2 = c3dObj.getContadorL()
                            c3dObj.addContadorL()
                            C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                            temporalL3 = c3dObj.getContadorL()
                            c3dObj.addContadorL()
                            if isinstance(resultado1C3D[1], list):
                                LV.extend(resultado1C3D[1])
                                LV.append(temporalL2)
                                LF.append(temporalL3)
                            else:
                                LV.append(resultado1C3D[1])
                                LV.append(temporalL2)
                                LF.append(temporalL3)
                        else:
                            C3D += resultado2C3D[0]
                            if isinstance(resultado1C3D[1], list):
                                LV.extend(resultado1C3D[1])
                                if isinstance(resultado2C3D[1], list):
                                    LV.extend(resultado2C3D[1])
                                else:
                                    LV.append(resultado2C3D[1])
                                if isinstance(resultado2C3D[2], list):
                                    LF.extend(resultado2C3D[2])
                                else:
                                    LF.append(resultado2C3D[2])
                            else:
                                LV.append(resultado1C3D[1])
                                if isinstance(resultado2C3D[1], list):
                                    LV.extend(resultado2C3D[1])
                                else:
                                    LV.append(resultado2C3D[1])
                                if isinstance(resultado2C3D[2], list):
                                    LF.extend(resultado2C3D[2])
                                else:
                                    LF.append(resultado2C3D[2])
        # OPERACION NOT
        elif self.operator == OPERADOR_LOGICO.NOT:
            if self.operating1.type == TIPO_DATO.BOOLEANO:
                self.type = TIPO_DATO.BOOLEANO
                resultado1C3D = self.operating1.getC3D(c3dObj)
                if isinstance(self.operating1, Primitivo):
                    C3D += resultado1C3D
                    C3D += c3dObj.endString()
                    C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                    temporalAux1 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                    temporalT2 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                    C3D += c3dObj.chargeTrue()
                    C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                    temporalAux1 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 1;\n"
                    temporalT2 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                    C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                    C3D += "    compareString();\n"
                    C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                    temporalT3 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                    temporalT4 = c3dObj.getContadorT()
                    c3dObj.addContadorT()
                    C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                    C3D += "    if t" + str(temporalT4) + " == 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                    temporalL0 = c3dObj.getContadorL()
                    c3dObj.addContadorL()
                    C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                    temporalL1 = c3dObj.getContadorL()
                    c3dObj.addContadorL()
                    LV.append(temporalL1)
                    LF.append(temporalL0)
                else:
                    C3D += resultado1C3D[0]
                    if isinstance(resultado1C3D[2], list):
                        LV.extend(resultado1C3D[2])
                        if isinstance(resultado1C3D[1], list):
                            LF.extend(resultado1C3D[1])
                        else:
                            LF.append(resultado1C3D[1])
                    else:
                        LV.append(resultado1C3D[2])
                        if isinstance(resultado1C3D[1], list):
                            LF.extend(resultado1C3D[1])
                        else:
                            LF.append(resultado1C3D[1])
        return [C3D, LV, LF]