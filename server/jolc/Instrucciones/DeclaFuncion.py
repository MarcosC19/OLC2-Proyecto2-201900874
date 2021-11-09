from Expresiones.Parametro import Parametro
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Excepciones.Excepcion import Excepcion

class Funcion(AST):

    def __init__(self, type, line, column, identifier, params, instructions):
        super().__init__(type, line, column)
        self.identificador = identifier
        self.parametros = params
        self.instrucciones = instructions

    def getNode(self):
        node = nodeAST("FUNCION")
        node.addChild("function")
        node.addChild(self.identificador)
        node.addChild("(")
        if self.parametros != None:
            for parametro in self.parametros:
                if isinstance(parametro, Parametro):
                    node.addChildrenNode(parametro.getNode())
                else:
                    idNode = nodeAST("IDENTIFICADOR")
                    idNode.addChildrenNode(parametro.getNode())
                    node.addChildrenNode(idNode)
                if parametro != self.parametros[-1]:
                    node.addChild(",")
        node.addChild(")")
        nodeInstrucion = nodeAST("INSTRUCCIONES")
        for instruccion in self.instrucciones:
            if isinstance(instruccion, Excepcion): continue
            nodeInstrucion.addChildrenNode(instruccion.getNode())
        node.addChildrenNode(nodeInstrucion)
        node.addChild("end;")
        return node

    def interpretar(self, table, tree):
        return self

    def getC3D(self, c3dObj):
        C3D = "    /* DECLARACION DE FUNCION */\n"


        return C3D