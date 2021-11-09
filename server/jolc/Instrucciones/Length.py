from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion
from tablaSimbolos.Tipo import TIPO_DATO

class Length(AST):

    def __init__(self, type, line, column, expression):
        super().__init__(type, line, column)
        self.expresion = expression

    def getNode(self):
        node = nodeAST("LENGTH")
        node.addChild("length")
        node.addChild("(")
        node.addChildrenNode(self.expresion.getNode())
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        value = self.expresion.interpretar(table, tree)
        if isinstance(value, Primitivo):
            value = value.interpretar(table, tree)
        
        if isinstance(value, str) or isinstance(value, list):
            return len(value)

        return Excepcion("Semantico", "El valor ingresado no posee longitud", self.line, self.column)

    def getC3D(self, c3dObj):
        C3D = "    /* LENGTH */\n"
        contadorR = 0
        if isinstance(self.expresion, list):
            C3D += "    t" + str(c3dObj.getContadorT()) + " = " + str(len(self.expresion)) + ";\n"
            contadorR = c3dObj.getContadorT()
            c3dObj.addContadorT()
        elif isinstance(self.expresion, Primitivo) and self.expresion.type == TIPO_DATO.CADENA:
            valor = self.expresion.interpretar(None, None)
            C3D += "    t" + str(c3dObj.getContadorT()) + " = " + str(len(valor)) + ";\n"
            contadorR = c3dObj.getContadorT()
            c3dObj.addContadorT()
        else:
            resultado = self.expresion.getC3D(c3dObj)
            C3D += resultado[0]
            
            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
            temporalT1 = c3dObj.getLastContadorT()
            temporalT2 = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += "    t" + str(c3dObj.getContadorT()) + " = t" + str(temporalT2) + " + 0;\n"
            temporalT3 = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += "    stack[int(t" + str(temporalT3) + ")] = t" + str(resultado[1]) + ";\n"
            C3D += "    P = P + " + str(c3dObj.getNumVariables()) + ";\n"
            C3D += "    getLength();\n"
            C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(P)];\n"
            temporalAux = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += "    t" + str(c3dObj.getContadorT()) + " = P + 1;\n"
            temporalAux1 = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporalAux1)  +")];\n"
            temporalAux2 = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += "    P = P - " + str(c3dObj.getNumVariables()) + ";\n"

            contadorR = temporalAux2
        return [C3D, contadorR]