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
        return ""