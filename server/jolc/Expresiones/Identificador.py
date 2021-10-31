from tablaSimbolos.Tipo import TIPO_DATO
from Excepciones.Excepcion import Excepcion
from Abstract.nodoAST import nodeAST
from Abstract.AST import AST
from Expresiones.Primitivo import Primitivo
from C3D.variableC3D import VariableC3D


class Identificador(AST):

    def __init__(self, type, line, column, identifier):
        super().__init__(type, line, column)
        self.identificador = identifier

    def getIdentifier(self):
        return self.identificador

    def getNode(self):
        node = nodeAST("IDENTIFICADOR")
        node.addChild(self.identificador)
        return node

    def interpretar(self, table, tree):
        simbolo = table.getVariable(self.identificador)
        if simbolo == None:
            return Excepcion("Semantico", "La variable " + str(self.identificador) + " no ha sido creada", self.line, self.column)
        self.type = simbolo.type
        if simbolo.type == TIPO_DATO.STRUCTN or simbolo.type == TIPO_DATO.STRUCTM or isinstance(simbolo.type, str):
            myStruct = simbolo
            return myStruct
        return simbolo.getValor()

    def getC3D(self, c3dObj):
        C3D = "    /* OBTENIENDO VARIABLE */\n"
        myVar = c3dObj.getVariable(self.identificador)
        temporalTV = None
        if myVar != None:
            self.type = myVar.typeVal
            C3D += "    t" + str(c3dObj.getContadorT()) + " = " + myVar.getPosition() + ";\n"
            temporalT0 = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalT0) + ")];\n"
            temporalTV = c3dObj.getContadorT()
            c3dObj.addContadorT()
            return [C3D, temporalTV, myVar.type, myVar.typeVal]
        return None