from Expresiones.Primitivo import Primitivo
from tablaSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Instrucciones.AsignStructN import StructN

class Asignacion(AST):
    
    def __init__(self, line, column, identifier, expression, type = None):
        super().__init__(type, line, column)
        self.identificador = identifier
        self.expresion = expression

    def getNode(self):
        node = nodeAST("ASIGNACION")
        node.addChild(self.identificador)
        node.addChild("=")
        node.addChildrenNode(self.expresion.getNode())
        if self.type != None:
            node.addChild("::")
            if self.type == TIPO_DATO.ENTERO: node.addChild("Int64")
            elif self.type == TIPO_DATO.DECIMAL: node.addChild("Float64")
            elif self.type == TIPO_DATO.CARACTER: node.addChild("Char")
            elif self.type == TIPO_DATO.CADENA: node.addChild("String")
            elif self.type == TIPO_DATO.BOOLEANO: node.addChild("Bool")
            elif self.type == TIPO_DATO.NULL: node.addChild("Null")
            elif self.type == TIPO_DATO.STRUCTN: node.addChild("STRUCT")
            elif self.type == TIPO_DATO.STRUCTM: node.addChild("STRUCT MUTABLE")
            else: node.addChild(self.type)

        return node

    def interpretar(self, table, tree):
        value = self.expresion.interpretar(table, tree)
        simbolo = None
        if isinstance(value, Excepcion): return value

        if not isinstance(self.type, str):
            if self.expresion.type != self.type and self.type !=None:
                if isinstance(value, Primitivo):
                    if value.type != self.type and self.type != None:
                        return Excepcion("Semantico", "Los tipos deben ser los mismos", self.line, self.column)
                else:
                    return Excepcion("Semantico", "Los tipos deben ser los mismos", self.line, self.column)
            if isinstance(value, Primitivo):
                self.type = value.type
                simbolo = Simbolo(self.type, self.identificador, self.line, self.column, value)
            else:
                if isinstance(value, Simbolo):
                    self.type = value.type
                else:
                    self.type = self.expresion.type
                valor = Primitivo(self.expresion.type, self.line, self.column, value)
                value = valor
                simbolo = Simbolo(self.type, self.identificador, self.line, self.column, valor)
        else:
            myStruct = table.getVariable(self.type)
            if myStruct == None:
                return Excepcion("Semantico", "El tipo ingresado no es valido", self.line, self.column)
            else:
                myType = myStruct.getId()
                if not isinstance(value, Simbolo):
                    if myType != self.expresion.identificador:
                        return Excepcion("Semantico", "Los tipos deben ser los mismos", self.line, self.column)
                    else:
                        valor = Primitivo(self.expresion.type, self.line, self.column, value)
                        value = valor
                        simbolo = Simbolo(self.type, self.identificador, self.line, self.column, valor)
                else:
                    if myType != value.id:
                        return Excepcion("Semantico", "Los tipos deben ser los mismos", self.line, self.column)
                    else:
                        value = value.getValor()
                        valor = Primitivo(self.expresion.type, self.line, self.column, value)
                        value = valor
                        simbolo = Simbolo(self.type, self.identificador, self.line, self.column, valor)

        variable = table.getVariable(simbolo.getId())
        if variable == None:
            asign = table.setVariable(simbolo)
            if asign != None:
                return asign
        else:
            if isinstance(variable.getTipo(), str): 
                simbolo.setTipo(variable.getTipo())
                self.type = simbolo.getTipo()
            variable.setValor(value)
            variable.setTipo(self.type)

        return None

    def getC3D(self, contador):
        return ""