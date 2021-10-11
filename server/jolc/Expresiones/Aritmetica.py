from Instrucciones.Return import Return
from tablaSimbolos.Tipo import TIPO_DATO
from Expresiones.Primitivo import Primitivo
from tablaSimbolos.Tipo import OPERADOR_ARITMETICO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Excepciones.Excepcion import Excepcion
import math

class Aritmetica(AST):

    def __init__(self, type, line, column, operator, operating1, operating2 = None):
        super().__init__(type, line, column)
        self.operator = operator
        self.operating1 = operating1
        self.operating2 = operating2

    def getNode(self):
        node = nodeAST("ARITMETICA")
        if(self.operating2 == None):
            if(self.operator == OPERADOR_ARITMETICO.UMENOS):
                node.addChild("-")
                node.addChildrenNode(self.operating1.getNode())
            elif(self.operator == OPERADOR_ARITMETICO.LOG10):
                node.addChild("log10")
                node.addChild("(")
                node.addChildrenNode(self.operating1.getNode())
                node.addChild(")")
            elif(self.operator == OPERADOR_ARITMETICO.SENO):
                node.addChild("sin")
                node.addChild("(")
                node.addChildrenNode(self.operating1.getNode())
                node.addChild(")")
            elif(self.operator == OPERADOR_ARITMETICO.COSENO):
                node.addChild("cos")
                node.addChild("(")
                node.addChildrenNode(self.operating1.getNode())
                node.addChild(")")
            elif(self.operator == OPERADOR_ARITMETICO.TANGENTE):
                node.addChild("tan")
                node.addChild("(")
                node.addChildrenNode(self.operating1.getNode())
                node.addChild(")")
            elif(self.operator == OPERADOR_ARITMETICO.RAIZ):
                node.addChild("sqrt")
                node.addChild("(")
                node.addChildrenNode(self.operating1.getNode())
                node.addChild(")")
        else:
            if(self.operator == OPERADOR_ARITMETICO.LOG):
                node.addChild("log")
                node.addChild("(")
                node.addChildrenNode(self.operating1.getNode())
                node.addChild(",")
                node.addChildrenNode(self.operating2.getNode())
                node.addChild(")")
                return node
            node.addChildrenNode(self.operating1.getNode())
            if(self.operator == OPERADOR_ARITMETICO.SUMA): node.addChild("+")
            elif(self.operator == OPERADOR_ARITMETICO.RESTA): node.addChild("-")
            elif(self.operator == OPERADOR_ARITMETICO.MULTIPLICACION): node.addChild("*")
            elif(self.operator == OPERADOR_ARITMETICO.DIVISON): node.addChild("/")
            elif(self.operator == OPERADOR_ARITMETICO.POTENCIA): node.addChild("^")
            elif(self.operator == OPERADOR_ARITMETICO.MODULO): node.addChild("%")
            node.addChildrenNode(self.operating2.getNode())
        return node
    
    def interpretar(self, table, tree):
        izquierdo = None
        derecho = None
        # INTERPRETANDO OPERANDOS
        if(self.operating2 == None):
            izquierdo = self.operating1.interpretar(table, tree)
            if isinstance(izquierdo, Excepcion): return izquierdo
            if isinstance(izquierdo, Return):
                izquierdo = izquierdo.interpretar(table, tree)
            if isinstance(izquierdo, Primitivo): 
                self.operating1.type = izquierdo.type
                izquierdo = izquierdo.interpretar(table, tree)
        else:
            izquierdo = self.operating1.interpretar(table, tree)
            if isinstance(izquierdo, Excepcion): return izquierdo
            if isinstance(izquierdo, Return):
                izquierdo = izquierdo.interpretar(table, tree)
            if isinstance(izquierdo, Primitivo):  
                self.operating1.type = izquierdo.type
                izquierdo = izquierdo.interpretar(table, tree)
            derecho = self.operating2.interpretar(table, tree)
            if isinstance(derecho, Excepcion): return derecho
            if isinstance(derecho, Return):
                derecho = derecho.interpretar(table, tree)
            if isinstance(derecho, Primitivo):  
                self.operating2.type = derecho.type
                derecho = derecho.interpretar(table, tree)
        # RETORNANDO VALORES
        # OPERACION SUMA
        if self.operator == OPERADOR_ARITMETICO.SUMA:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:   # ENTERO + ENTERO
                    self.type = TIPO_DATO.ENTERO
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) + int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # ENTERO + DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) + float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para +" , self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:   # DECIMAL + ENTERO
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) + int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # DECIMAL + DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) + float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para +" , self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para +" , self.line, self.column)
        # OPERACION RESTA
        elif self.operator == OPERADOR_ARITMETICO.RESTA:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:   # ENTERO - ENTERO
                    self.type = TIPO_DATO.ENTERO
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) - int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # ENTERO - DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) - float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para -" , self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:   # DECIMAL - ENTERO
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) - int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # DECIMAL - DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) - float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para -" , self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para -" , self.line, self.column)
        # OPERACION MULTIPLICACION
        elif self.operator == OPERADOR_ARITMETICO.MULTIPLICACION:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:   # ENTERO * ENTERO
                    self.type = TIPO_DATO.ENTERO
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) * int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # ENTERO * DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) * float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para *" , self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:   # DECIMAL * ENTERO
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) * int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # DECIMAL * DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) * float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para *" , self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.CADENA:
                    self.type = TIPO_DATO.CADENA
                    return Primitivo(self.type, self.line, self.column, str(izquierdo) + str(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para *" , self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para *" , self.line, self.column)
        # OPERACION DIVISION
        elif self.operator == OPERADOR_ARITMETICO.DIVISON:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:   # ENTERO / ENTERO
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) / int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # ENTERO / DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) / float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para /" , self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:   # DECIMAL / ENTERO
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) / int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # DECIMAL / DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) / float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para /" , self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para /" , self.line, self.column)
        # OPERACION POTENCIA
        elif self.operator == OPERADOR_ARITMETICO.POTENCIA:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:   # ENTERO ^ ENTERO
                    self.type = TIPO_DATO.ENTERO
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) ** int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # ENTERO ^ DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) ** float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para ^" , self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:   # DECIMAL ^ ENTERO
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) ** int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # DECIMAL ^ DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) ** float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para ^" , self.line, self.column)
            elif self.operating1.type == TIPO_DATO.CADENA:
                if self.operating2.type == TIPO_DATO.ENTERO:
                    self.type = TIPO_DATO.CADENA
                    cadenaN = ""
                    for i in range(derecho):
                        cadenaN += izquierdo
                    return Primitivo(self.type, self.line, self.column, cadenaN)
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para ^" , self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para ^" , self.line, self.column)
        # OPERACION MODULO
        elif self.operator == OPERADOR_ARITMETICO.MODULO:
            if self.operating1.type == TIPO_DATO.ENTERO:
                if self.operating2.type == TIPO_DATO.ENTERO:   # ENTERO % ENTERO
                    self.type = TIPO_DATO.ENTERO
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) % int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # ENTERO % DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, int(izquierdo) % float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para %" , self.line, self.column)
            elif self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO:   # DECIMAL % ENTERO
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) % int(derecho))
                elif self.operating2.type == TIPO_DATO.DECIMAL:  # DECIMAL % DECIMAL
                    self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, float(izquierdo) % float(derecho))
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para %" , self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para %" , self.line, self.column)
        # FUNCION NATIVAS

        # LOGARITMO BASE 10
        elif self.operator == OPERADOR_ARITMETICO.LOG10:
            if self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL:
                resultado = math.log10(izquierdo)
                if isinstance(resultado, int):
                    self.type = TIPO_DATO.ENTERO
                elif isinstance(resultado, float):
                    self.type = TIPO_DATO.DECIMAL
                return Primitivo(self.type, self.line, self.column, resultado)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para log10" , self.line, self.column)
        # LOGARITMO BASE DIFERENTE
        elif self.operator == OPERADOR_ARITMETICO.LOG:
            if self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL:
                if self.operating2.type == TIPO_DATO.ENTERO or self.operating2.type == TIPO_DATO.DECIMAL:
                    resultado = math.log(derecho, izquierdo)
                    if isinstance(resultado, int):
                        self.type = TIPO_DATO.ENTERO
                    elif isinstance(resultado, float):
                        self.type = TIPO_DATO.DECIMAL
                    return Primitivo(self.type, self.line, self.column, resultado)
                else:
                    return Excepcion("Semantico", "Operando 2 no valido para log" , self.line, self.column)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para log" , self.line, self.column)
        # SENO DE UN GRADO
        elif self.operator == OPERADOR_ARITMETICO.SENO:
            if self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL:
                resultado = math.sin(izquierdo)
                if isinstance(resultado, int):
                    self.type = TIPO_DATO.ENTERO
                elif isinstance(resultado, float):
                    self.type = TIPO_DATO.DECIMAL
                return Primitivo(self.type, self.line, self.column, resultado)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para sin" , self.line, self.column)
        # COSENO DE UN GRADO
        elif self.operator == OPERADOR_ARITMETICO.COSENO:
            if self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL:
                resultado = math.cos(izquierdo)
                if isinstance(resultado, int):
                    self.type = TIPO_DATO.ENTERO
                elif isinstance(resultado, float):
                    self.type = TIPO_DATO.DECIMAL
                return Primitivo(self.type, self.line, self.column, resultado)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para sin" , self.line, self.column)
        # TANGENTE DE UN GRADO
        elif self.operator == OPERADOR_ARITMETICO.TANGENTE:
            if self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL:
                resultado = math.tan(izquierdo)
                if isinstance(resultado, int):
                    self.type = TIPO_DATO.ENTERO
                elif isinstance(resultado, float):
                    self.type = TIPO_DATO.DECIMAL
                return Primitivo(self.type, self.line, self.column, resultado)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para sin" , self.line, self.column)
        # RAIZ CUADRADA
        elif self.operator == OPERADOR_ARITMETICO.RAIZ:
            if self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL:
                resultado = math.sqrt(izquierdo)
                if isinstance(resultado, int):
                    self.type = TIPO_DATO.ENTERO
                elif isinstance(resultado, float):
                    self.type = TIPO_DATO.DECIMAL
                return Primitivo(self.type, self.line, self.column, resultado)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para sin" , self.line, self.column)
        # OPERADOR UNARIO "-"
        elif self.operator == OPERADOR_ARITMETICO.UMENOS:
            if self.operating1.type == TIPO_DATO.ENTERO or self.operating1.type == TIPO_DATO.DECIMAL:
                resultado = -1 * izquierdo
                if isinstance(resultado, int):
                    self.type = TIPO_DATO.ENTERO
                elif isinstance(resultado, float):
                    self.type = TIPO_DATO.DECIMAL
                return Primitivo(self.type, self.line, self.column, resultado)
            else:
                return Excepcion("Semantico", "Operando 1 no valido para unario" , self.line, self.column)
        # CUALQUIER OTRO
        else:
            return Excepcion("Semantico", "Operador no valido", self.line, self.column)

    def getC3D(self, contador):
        C3D = ""
        if isinstance(self.operating1, Primitivo):
            valores = self.operating1.getC3D(contador)
            for valor in valores:
                C3D += "    t" + str(contador) + " = " + str(valor)
        if self.operator == OPERADOR_ARITMETICO.SUMA:
            C3D += " + "
        if isinstance(self.operating2, Primitivo):
            valores = self.operating2.getC3D(contador)
            for valor in valores:
                C3D += str(valor) + ";"
        contador += 1
        return [C3D, contador]