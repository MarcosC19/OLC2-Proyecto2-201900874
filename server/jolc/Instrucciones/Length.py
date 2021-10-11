from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Expresiones.Primitivo import Primitivo
from Excepciones.Excepcion import Excepcion

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

    def getC3D(self, contador):
        return ""