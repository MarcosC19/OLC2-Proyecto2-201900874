from Expresiones.Parametro import Parametro
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST
from Excepciones.Excepcion import Excepcion
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.If import If
from Instrucciones.AsignacionVar import Asignacion
from C3D.sentC3D import C3DT
from C3D.variableC3D import VariableC3D
from C3D.variableC3D import TipoVar
from C3D.variableC3D import TipoVariable
from Instrucciones.Return import Return
from tablaSimbolos.Tipo import TIPO_DATO

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
        c3dNuevo = C3DT()
        c3dNuevo.funciones = c3dObj.funciones
        C3D1 = "/* DECLARACION DE FUNCION */\n"
        C3D1 += "func " + str(self.identificador) + "(){\n"

        if self.parametros is not None:

            for parametro in self.parametros:
                tiponewVal = TIPO_DATO.DECIMAL
                tipoValnew = TipoVariable.VARIABLE
                tipoApunt = TipoVar.VALOR
                if isinstance(parametro, Parametro):
                    tiponewVal = parametro.getType()

                if tiponewVal == TIPO_DATO.LISTA or tiponewVal == TIPO_DATO.CADENA:
                    tipoApunt = TipoVar.APUNTADOR
                    if tiponewVal == TIPO_DATO.LISTA:
                        tipoValnew = TipoVariable.LISTA
                newVariable = VariableC3D(parametro.getIdentifier(), "P + " + str(c3dNuevo.getNumVariables()), tipoApunt, tiponewVal, tipoValnew)
                
                c3dNuevo.addVariable(newVariable.getName(), newVariable)
                c3dNuevo.addNumVariable()
                
        for instruccion in self.instrucciones:
            if isinstance(instruccion, Break):
                C3D1 += instruccion.getC3D(c3dNuevo, None)
            elif isinstance(instruccion, Continue):
                C3D1 += instruccion.getC3D(c3dNuevo, None)
            elif isinstance(instruccion, If):
                C3D1 += instruccion.getC3D(c3dNuevo, None, None)
            elif isinstance(instruccion, Asignacion):
                C3D1 += instruccion.getC3D(c3dNuevo)
            else:
                C3D1 += instruccion.getC3D(c3dNuevo)
        C3D1 += "    return;\n"
        C3D1 += "}\n\n"
        return C3D1