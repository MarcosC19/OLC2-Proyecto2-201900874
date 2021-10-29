from Expresiones.Identificador import Identificador
from Expresiones.Aritmetica import Aritmetica
from tablaSimbolos.Tipo import OPERADOR_ARITMETICO
from tablaSimbolos.Tipo import TIPO_DATO
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import OPERADOR_RELACIONAL
from Abstract.nodoAST import nodeAST
from Abstract.AST import AST


class Relacional(AST):

    def __init__(self, type, line, column, operator, operating1, operating2):
        super().__init__(type, line, column)
        self.operator = operator
        self.operating1 = operating1
        self.operating2 = operating2

    def getNode(self):
        node = nodeAST("RELACIONAL")
        node.addChildrenNode(self.operating1.getNode())
        if self.operator == OPERADOR_RELACIONAL.MAYORQUE: node.addChild(">")
        elif self.operator == OPERADOR_RELACIONAL.MENORQUE: node.addChild("<")
        elif self.operator == OPERADOR_RELACIONAL.MAYORIGUAL: node.addChild(">=")
        elif self.operator == OPERADOR_RELACIONAL.MENORIGUAL: node.addChild("<=")
        elif self.operator == OPERADOR_RELACIONAL.IGUAL: node.addChild("==")
        elif self.operator == OPERADOR_RELACIONAL.DIFERENTE: node.addChild("!=")
        node.addChildrenNode(self.operating2.getNode())
        return node

    def interpretar(self, table, tree):
        izquierdo = None
        derecho = None

        # INTERPRETANDO LOS OPERANDOS
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
        # OPERANDO MAYOR QUE >
        if self.operator == OPERADOR_RELACIONAL.MAYORQUE:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return int(izquierdo) > int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return int(izquierdo) > float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion >", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return float(izquierdo) > int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return float(izquierdo) > float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion >", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) > str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion >", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CARACTER:
                if self.operating2.type == TIPO_DATO.CARACTER:
                    return str(izquierdo) > str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion >", self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no es valido para la operacion >", self.line, self.column)
        # OPERANDO MENOR QUE <
        elif self.operator == OPERADOR_RELACIONAL.MENORQUE:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return int(izquierdo) < int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return int(izquierdo) < float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion <", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return float(izquierdo) < int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return float(izquierdo) < float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion <", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) < str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion <", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CARACTER:
                if self.operating2.type == TIPO_DATO.CARACTER:
                    return str(izquierdo) < str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion <", self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no es valido para la operacion <", self.line, self.column)
        # OPERANDO MAYOR IGUAL QUE >=
        elif self.operator == OPERADOR_RELACIONAL.MAYORIGUAL:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return int(izquierdo) >= int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return int(izquierdo) >= float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion >=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return float(izquierdo) >= int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return float(izquierdo) >= float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion >=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) >= str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion >=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CARACTER:
                if self.operating2.type == TIPO_DATO.CARACTER:
                    return str(izquierdo) >= str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion >=", self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no es valido para la operacion >=", self.line, self.column)
        # OPERANDO MENOR IGUAL QUE <=
        elif self.operator == OPERADOR_RELACIONAL.MENORIGUAL:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return int(izquierdo) <= int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return int(izquierdo) <= float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion <=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return float(izquierdo) <= int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return float(izquierdo) <= float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion <=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) <= str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion <=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CARACTER:
                if self.operating2.type == TIPO_DATO.CARACTER:
                    return str(izquierdo) <= str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion <=", self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no es valido para la operacion <=", self.line, self.column)
        # OPERANDO IGUAL IGUAL QUE ==
        elif self.operator == OPERADOR_RELACIONAL.IGUAL:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return int(izquierdo) == int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return int(izquierdo) == float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion ==", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return float(izquierdo) == int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return float(izquierdo) == float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion ==", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) == str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion ==", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CARACTER:
                if self.operating2.type == TIPO_DATO.CARACTER:
                    return str(izquierdo) == str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion ==", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.BOOLEANO:
                if self.operating2.type == TIPO_DATO.BOOLEANO:
                    return bool(izquierdo) == bool(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion ==", self.line, self.column)
            else:
                return bool(izquierdo == derecho)
        # OPERANDO DIFERENTE QUE !=
        elif self.operator == OPERADOR_RELACIONAL.DIFERENTE:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return int(izquierdo) != int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return int(izquierdo) != float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion !=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    return float(izquierdo) != int(derecho)
                elif self.operating2.type == TIPO_DATO.DECIMAL:
                    return float(izquierdo) != float(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion !=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) != str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion !=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CARACTER:
                if self.operating2.type == TIPO_DATO.CARACTER:
                    return str(izquierdo) != str(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion !=", self.line, self.column)
            elif self.operating1.type == TIPO_DATO.BOOLEANO:
                if self.operating2.type == TIPO_DATO.BOOLEANO:
                    return bool(izquierdo) != bool(derecho)
                else:
                    return Excepcion("Semantico", "Operando 2 no es valido para la operacion !=", self.line, self.column)
            else:
                return bool(izquierdo != derecho)
        # CUALQUIER OTRO
        else:
            return Excepcion("Semantico", "Operador no valido", self.line, self.column)

    def getC3D(self, c3dObj):
        C3D = "    /* ANALIZANDO EXPRESION RELACIONAL */\n"
        temporalL0 = ""
        temporalL1 = ""
        # OPERANDO MAYOR QUE >
        if self.operator == OPERADOR_RELACIONAL.MAYORQUE:
            if (self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL) and (self.operating2.type == TIPO_DATO.ENTERO or self.operating2.type == TIPO_DATO.DECIMAL) or isinstance(self.operating1, Identificador) or isinstance(self.operating2, Identificador):
                if isinstance(self.operating1, Primitivo):
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating2, Primitivo):  # PRIMITIVO > PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " > "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # PRIMITIVO > OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " > "
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "t" + str(resultado2C3D[1]) + " "
                            else:
                                C3D += "" + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                else:
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating1, Aritmetica):
                        if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                            C3D += resultado1C3D[0]
                    if isinstance(self.operating2, Primitivo):  # OTRO > PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "    if t" + str(resultado1C3D[1]) + " > "
                            else:
                                C3D += "    if " + str(resultado1C3D[0]) + " > "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # OTRO > OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " > t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " > " + str(resultado2C3D[0]) + " "
                            else:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if " + str(resultado1C3D[0]) + " > t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if " + str(resultado1C3D[0]) + " > " + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) > str(derecho)
        # OPERANDO MENOR QUE <
        elif self.operator == OPERADOR_RELACIONAL.MENORQUE:
            if (self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL) and (self.operating2.type == TIPO_DATO.ENTERO or self.operating2.type == TIPO_DATO.DECIMAL) or isinstance(self.operating1, Identificador) or isinstance(self.operating2, Identificador):
                if isinstance(self.operating1, Primitivo):
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating2, Primitivo):  # PRIMITIVO < PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " < "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # PRIMITIVO < OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " < "
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "t" + str(resultado2C3D[1]) + " "
                            else:
                                C3D += "" + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                else:
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating1, Aritmetica):
                        if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                            C3D += resultado1C3D[0]
                    if isinstance(self.operating2, Primitivo):  # OTRO < PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "    if t" + str(resultado1C3D[1]) + " < "
                            else:
                                C3D += "    if " + str(resultado1C3D[0]) + " < "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # OTRO < OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " < t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " < " + str(resultado2C3D[0]) + " "
                            else:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if " + str(resultado1C3D[0]) + " < t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if " + str(resultado1C3D[0]) + " < " + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) < str(derecho)
        # OPERANDO MAYOR IGUAL QUE >=
        elif self.operator == OPERADOR_RELACIONAL.MAYORIGUAL:
            if (self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL) and (self.operating2.type == TIPO_DATO.ENTERO or self.operating2.type == TIPO_DATO.DECIMAL) or isinstance(self.operating1, Identificador) or isinstance(self.operating2, Identificador):
                if isinstance(self.operating1, Primitivo):
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating2, Primitivo):  # PRIMITIVO >= PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " >= "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # PRIMITIVO >= OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " >= "
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "t" + str(resultado2C3D[1]) + " "
                            else:
                                C3D += "" + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                else:
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating1, Aritmetica):
                        if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                            C3D += resultado1C3D[0]
                    if isinstance(self.operating2, Primitivo):  # OTRO >= PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "    if t" + str(resultado1C3D[1]) + " >= "
                            else:
                                C3D += "    if " + str(resultado1C3D[0]) + " >= "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # OTRO >= OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " >= t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " >= " + str(resultado2C3D[0]) + " "
                            else:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if " + str(resultado1C3D[0]) + " >= t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if " + str(resultado1C3D[0]) + " >= " + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) >= str(derecho)
        # OPERANDO MENOR IGUAL QUE <=
        elif self.operator == OPERADOR_RELACIONAL.MENORIGUAL:
            if (self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL) and (self.operating2.type == TIPO_DATO.ENTERO or self.operating2.type == TIPO_DATO.DECIMAL) or isinstance(self.operating1, Identificador) or isinstance(self.operating2, Identificador):
                if isinstance(self.operating1, Primitivo):
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating2, Primitivo):  # PRIMITIVO <= PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " <= "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # PRIMITIVO <= OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " <= "
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "t" + str(resultado2C3D[1]) + " "
                            else:
                                C3D += "" + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                else:
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating1, Aritmetica):
                        if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                            C3D += resultado1C3D[0]
                    if isinstance(self.operating2, Primitivo):  # OTRO <= PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "    if t" + str(resultado1C3D[1]) + " <= "
                            else:
                                C3D += "    if " + str(resultado1C3D[0]) + " <= "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # OTRO <= OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " <= t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " <= " + str(resultado2C3D[0]) + " "
                            else:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if " + str(resultado1C3D[0]) + " <= t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if " + str(resultado1C3D[0]) + " <= " + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    return str(izquierdo) <= str(derecho)
        # OPERANDO IGUAL IGUAL QUE ==
        elif self.operator == OPERADOR_RELACIONAL.IGUAL:
            if (self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL) or (self.operating2.type == TIPO_DATO.ENTERO or self.operating2.type == TIPO_DATO.DECIMAL) or isinstance(self.operating1, Identificador) or isinstance(self.operating2, Identificador):
                if isinstance(self.operating1, Primitivo):
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating2, Primitivo):  # PRIMITIVO == PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " == "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # PRIMITIVO == OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " == "
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "t" + str(resultado2C3D[1]) + " "
                            else:
                                C3D += "" + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                else:
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating1, Aritmetica):
                        if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                            C3D += resultado1C3D[0]
                    if isinstance(self.operating2, Primitivo):  # OTRO == PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "    if t" + str(resultado1C3D[1]) + " == "
                            else:
                                C3D += "    if " + str(resultado1C3D[0]) + " == "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # OTRO == OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " == t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " == " + str(resultado2C3D[0]) + " "
                            else:
                                if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                    C3D += "    if " + str(resultado1C3D[0]) + " == t" + str(resultado2C3D[1]) + " "
                                else:
                                    C3D += "    if " + str(resultado1C3D[0]) + " == " + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
            elif (self.operating1.type == TIPO_DATO.CADENA and self.operating2.type == TIPO_DATO.CADENA) or (self.operating1.type == TIPO_DATO.BOOLEANO and self.operating2.type == TIPO_DATO.BOOLEANO):
                if isinstance(self.operating1, Primitivo):
                    if isinstance(self.operating2, Primitivo):
                        C3D += self.operating1.getC3D(c3dObj)
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux1 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += self.operating2.getC3D(c3dObj)
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux2 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 1;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
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

                else:
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    C3D += resultado1C3D[0]
                    C3D += "    L" + str(resultado1C3D[1]) + ":\n"
                   
                    if isinstance(self.operating2, Primitivo):
                        C3D += c3dObj.saveString("true")
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux1 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += self.operating2.getC3D(c3dObj)
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux2 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 1;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
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
                    else:
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        C3D += resultado2C3D[0]
                        C3D += "    L" + str(resultado2C3D[1]) + ":\n"
                        C3D += c3dObj.saveString("true")
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux1 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += c3dObj.saveString("true")
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux2 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 1;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
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
                        C3D += "    L" + str(resultado2C3D[2]) + ":\n"
                        C3D += c3dObj.saveString("false")


                    C3D += "    L" + str(resultado1C3D[2]) + ":\n"
                    C3D += c3dObj.saveString("false")
        # OPERANDO DIFERENTE QUE !=
        elif self.operator == OPERADOR_RELACIONAL.DIFERENTE:
            if (self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL) and (self.operating2.type == TIPO_DATO.ENTERO or self.operating2.type == TIPO_DATO.DECIMAL) or isinstance(self.operating1, Identificador) or isinstance(self.operating2, Identificador):
                if isinstance(self.operating1, Primitivo):
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating2, Primitivo):  # PRIMITIVO != PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " != "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # PRIMITIVO != OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        for contenido in resultado1C3D:
                            C3D += "    if " + str(contenido) + " != "
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "t" + str(resultado2C3D[1]) + " "
                            else:
                                C3D += "" + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                else:
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    if isinstance(self.operating1, Aritmetica):
                        if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                            C3D += resultado1C3D[0]
                    if isinstance(self.operating2, Primitivo):  # OTRO != PRIMITIVO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += "    if t" + str(resultado1C3D[1]) + " != "
                            else:
                                C3D += "    if " + str(resultado1C3D[1]) + " != "
                        for contenido in resultado2C3D:
                            C3D += str(contenido) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:                                   # OTRO != OTRO
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        if isinstance(self.operating2, Aritmetica):
                            if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                C3D += resultado2C3D[0]
                        if isinstance(self.operating1, Aritmetica):
                            if self.operating1.operator != OPERADOR_ARITMETICO.UMENOS:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " != t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if t" + str(resultado1C3D[1]) + " != " + str(resultado2C3D[0]) + " "
                            else:
                                if isinstance(self.operating2, Aritmetica):
                                    if self.operating2.operator != OPERADOR_ARITMETICO.UMENOS:
                                        C3D += "    if " + str(resultado1C3D[0]) + " != t" + str(resultado2C3D[1]) + " "
                                    else:
                                        C3D += "    if " + str(resultado1C3D[0]) + " != " + str(resultado2C3D[0]) + " "
                        C3D += "{ goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
            elif (self.operating1.type == TIPO_DATO.CADENA and self.operating2.type == TIPO_DATO.CADENA) or (self.operating1.type == TIPO_DATO.BOOLEANO and self.operating2.type == TIPO_DATO.BOOLEANO):
                if isinstance(self.operating1, Primitivo):
                    if isinstance(self.operating2, Primitivo):
                        C3D += self.operating1.getC3D(c3dObj)
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux1 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += self.operating2.getC3D(c3dObj)
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux2 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 1;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
                        C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    compareString();\n"
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                        temporalT3 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                        temporalT4 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    if t" + str(temporalT4) + " != 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                else:
                    resultado1C3D = self.operating1.getC3D(c3dObj)
                    C3D += resultado1C3D[0]
                    C3D += "    L" + str(resultado1C3D[1]) + ":\n"
                    if isinstance(self.operating2, Primitivo):
                        C3D += c3dObj.saveString("true")
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux1 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += self.operating2.getC3D(c3dObj)
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux2 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 1;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
                        C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    compareString();\n"
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                        temporalT3 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                        temporalT4 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    if t" + str(temporalT4) + " != 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                    else:
                        resultado2C3D = self.operating2.getC3D(c3dObj)
                        C3D += resultado2C3D[0]
                        C3D += "    L" + str(resultado2C3D[1]) + ":\n"
                        C3D += c3dObj.saveString("true")
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux1 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux1) + " + 0;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux1 - 1) + ";\n"
                        C3D += c3dObj.saveString("true")
                        C3D += c3dObj.endString()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        c3dObj.addContadorT()
                        temporalAux2 = c3dObj.getLastContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalAux2) + " + 1;\n"
                        temporalT2 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    stack[int(t" + str(temporalT2) + ")] = t" + str(temporalAux2 - 1) + ";\n"
                        C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    compareString();\n"
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 2;\n"
                        temporalT3 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
                        temporalT4 = c3dObj.getContadorT()
                        c3dObj.addContadorT()
                        C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"
                        C3D += "    if t" + str(temporalT4) + " != 1 { goto L" + str(c3dObj.getContadorL()) + "; }\n"
                        temporalL0 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
                        temporalL1 = c3dObj.getContadorL()
                        c3dObj.addContadorL()
                        C3D += "    L" + str(resultado2C3D[2]) + ":\n"
                        C3D += c3dObj.saveString("false")


                    C3D += "    L" + str(resultado1C3D[2]) + ":\n"
                    C3D += c3dObj.saveString("false")
                    
        return [C3D, temporalL0, temporalL1]    # RETORNO [C3D, ListaV, ListaF]