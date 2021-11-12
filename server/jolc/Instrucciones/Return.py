from Expresiones.Primitivo import Primitivo
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Identificador import Identificador
from tablaSimbolos.Tipo import TIPO_DATO
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class Return(AST):

    def __init__(self, line, column, expression):
        super().__init__(TIPO_DATO.NULL, line, column)
        self.expresion = expression

    def getNode(self):
        node = nodeAST("RETURN")
        node.addChild("return")
        node.addChildrenNode(self.expresion.getNode())
        node.addChild(";")
        return node

    def interpretar(self, table, tree):
        if isinstance(self.expresion, Primitivo):
            return self.expresion
        else:
            return self.expresion.interpretar(table, tree)

    def getC3D(self, c3dObj):
        C3DText = "    /* REALIZANDO RETURN */\n"
        C3DText += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables()) + ";\n"
        temporal1 = c3dObj.getContadorT()
        temporalesR = 1
        c3dObj.addContadorT()
        if isinstance(self.expresion, Primitivo):
            valor = self.expresion.getValue()
            if self.expresion.type != TIPO_DATO.CADENA:
                C3DText += "    stack[int(t" + str(temporal1) + ")] = " + str(valor) + ";\n"
        else:
            
            if isinstance(self.expresion, Primitivo) or isinstance(self.expresion, Aritmetica) or isinstance(self.expresion, Identificador):
                resultado = self.expresion.getC3D(c3dObj)
                C3DText += resultado[0]
                C3DText += "    stack[int(t" + str(temporal1) + ")] = t" + str(resultado[1]) + ";\n"
            else:  
                C3DText += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables() + temporalesR) + ";\n"
                temporal2 = c3dObj.getContadorT()
                c3dObj.addContadorT()
                C3DText += "    stack[int(t" + str(temporal2) + ")] = t" + str(temporal1) + ";\n"
                resultado = self.expresion.getC3D(c3dObj)
                C3DText += resultado[0]

                C3DText += "    t" + str(c3dObj.getContadorT()) + " = P + " + str(c3dObj.getNumVariables() + temporalesR) + ";\n"
                temporal3 = c3dObj.getContadorT()
                c3dObj.addContadorT()
                C3DText += "    t" + str(c3dObj.getContadorT()) + " = stack[int(t" + str(temporal3) + ")];\n"
                temporal4 = c3dObj.getContadorT()
                c3dObj.addContadorT()
                C3DText += "    t" + str(temporal1) + " = t" + str(temporal4) + ";\n"
                C3DText += "    stack[int(t" + str(temporal1) + ")] = t" + str(resultado[1]) + ";\n"

        C3DText += "    return;\n"
        return C3DText