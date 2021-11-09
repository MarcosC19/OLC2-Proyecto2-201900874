from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from tablaSimbolos.Tipo import TIPO_DATO
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion

class LowerCase(AST):

    def __init__(self, type, line, column, expression):
        super().__init__(type, line, column)
        self.expresion = expression

    def getNode(self):
        node = nodeAST("LOWERCASE")
        node.addChild("lowercase")
        node.addChild("(")
        node.addChildrenNode(self.expresion.getNode())
        node.addChild(")")
        return node

    def interpretar(self, table, tree):
        if self.expresion.type == TIPO_DATO.CADENA or self.expresion.type == TIPO_DATO.CARACTER:
            self.type = self.expresion.type
            value = self.expresion.interpretar(table, tree)
            if isinstance(value, Excepcion): return value
            if isinstance(value, Primitivo): value = value.interpretar(table, tree)
            return str(value).lower()
        else:
            return Excepcion("Semantico", "Se esperaba una cadena o caracter", self.line, self.column)

    def getC3D(self, c3dObj):
        contadorTP = c3dObj.getContadorT()
        C3D = "    /* LOWERCASE */\n"
        resultado = self.expresion.getC3D(c3dObj)

        if isinstance(self.expresion, Primitivo):
            C3D += resultado
            C3D += c3dObj.endString()
            C3D += "    t" + str(c3dObj.getContadorT()) + " = H;\n"
            contadorTP2 = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += c3dObj.printLower(contadorTP)
            C3D += c3dObj.endString()
            contadorTP = contadorTP2
        else:
            C3D += resultado[0]
            C3D += "    t" + str(c3dObj.getContadorT()) + " = H;\n"
            contadorTP2 = c3dObj.getContadorT()
            c3dObj.addContadorT()
            C3D += c3dObj.printLower(resultado[1])
            C3D += c3dObj.endString()
            contadorTP = contadorTP2
        return [C3D, contadorTP]