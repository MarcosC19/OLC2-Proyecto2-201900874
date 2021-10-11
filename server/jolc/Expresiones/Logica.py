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

    def getC3D(self, contador):
        return ""