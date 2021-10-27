from Expresiones.Primitivo import Primitivo
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from tablaSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from C3D.variableC3D import VariableC3D
from C3D.variableC3D import TipoVar

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

    def getC3D(self, c3dObj):
        C3D = "    /* ASIGNANDO VARIABLE */\n"
        C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
        temporalTPos = c3dObj.getContadorT()
        c3dObj.addContadorT()
        c3dObj.addNumVariable()
        myVariable = None
        temporalT0 = ""
        if isinstance(self.expresion, Primitivo):
            resultadoExpresion = self.expresion.getC3D(c3dObj)
            if isinstance(resultadoExpresion, list):
                for valor in resultadoExpresion:
                    C3D += "    t" + str(c3dObj.getContadorT()) + " = " + str(valor) + ";\n"
                temporalT0 = c3dObj.getContadorT()
                c3dObj.addContadorT()
                myVariable = VariableC3D(self.identificador, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.VALOR, self.expresion.type)
            else:
                C3D += resultadoExpresion
                C3D += c3dObj.endString()
                temporalT0 = c3dObj.getLastContadorT()
                myVariable = VariableC3D(self.identificador, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.APUNTADOR, self.expresion.type)
            C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(temporalT0)  + ";\n"
        elif isinstance(self.expresion, Aritmetica):
            contadorTP = c3dObj.getContadorT()
            resultadoExpresion = self.expresion.getC3D(c3dObj)
            temporalT0 = resultadoExpresion[1]
            if self.expresion.operating2 == None:
                C3D += "    stack[int(t" + str(temporalTPos) + ")] = " + str(resultadoExpresion[0])  + ";\n"
            else:
                C3D += resultadoExpresion[0]
                if self.expresion.type == TIPO_DATO.CADENA:
                    C3D += c3dObj.endString()
                    C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(contadorTP)  + ";\n"
                    myVariable = VariableC3D(self.identificador, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.APUNTADOR, self.expresion.type)
                else:
                    C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(temporalT0)  + ";\n"
                    myVariable = VariableC3D(self.identificador, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.VALOR, self.expresion.type)
        elif isinstance(self.expresion, Relacional):
            resultadoExpresion = self.expresion.getC3D(c3dObj)
            C3D += resultadoExpresion[0]
            C3D += "    L" + str(resultadoExpresion[1]) + ":\n"
            temporalT1 = c3dObj.getContadorT()
            C3D += c3dObj.saveString("true")
            C3D += c3dObj.endString()
            C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(temporalT1) + ";\n"
            C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
            temporalLS = c3dObj.getContadorL()
            c3dObj.addContadorL()
            C3D += "    L" + str(resultadoExpresion[2]) + ":\n"
            temporalT1 = c3dObj.getContadorT()
            C3D += c3dObj.saveString("false")
            C3D += c3dObj.endString()
            C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(temporalT1) + ";\n"
            C3D += "    L" + str(temporalLS) + ":\n"
            myVariable = VariableC3D(self.identificador, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.APUNTADOR, self.expresion.type)
        elif isinstance(self.expresion, Logica):
            resultadoExpresion = self.expresion.getC3D(c3dObj)
            C3D += resultadoExpresion[0]
            for valor in resultadoExpresion[1]:
                C3D += "    L" + str(valor) + ":\n"
            temporalT1 = c3dObj.getContadorT()
            C3D += c3dObj.saveString("true")
            C3D += c3dObj.endString()
            C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(temporalT1) + ";\n"
            C3D += "    goto L" + str(c3dObj.getContadorL()) + ";\n"
            temporalLS = c3dObj.getContadorL()
            c3dObj.addContadorL()
            for valor in resultadoExpresion[2]:
                C3D += "    L" + str(valor) + ":\n"
            temporalT1 = c3dObj.getContadorT()
            C3D += c3dObj.saveString("false")
            C3D += c3dObj.endString()
            C3D += "    stack[int(t" + str(temporalTPos) + ")] = t" + str(temporalT1) + ";\n"
            C3D += "    L" + str(temporalLS) + ":\n"
            myVariable = VariableC3D(self.identificador, "P + " + str(c3dObj.getNumVariables() - 1), TipoVar.APUNTADOR, self.expresion.type)
        if myVariable != None:
            c3dObj.addVariable(myVariable.getName(), myVariable)
        return C3D