from Instrucciones.Return import Return
from Instrucciones.GlobalVar import Global
from Instrucciones.If import If
from Instrucciones.Continue import Continue
from Instrucciones.Break import Break
from tablaSimbolos.Tabla import Tabla
from tablaSimbolos.Tipo import TIPO_DATO
from Excepciones.Excepcion import Excepcion
from Abstract.AST import AST
from Abstract.nodoAST import nodeAST

class While(AST):

    def __init__(self, type, line, column, condition, instructions):
        super().__init__(type, line, column)
        self.condicion = condition
        self.instrucciones = instructions

    def getNode(self):
        nodeWhile = nodeAST("WHILE")

        nodeExp = nodeAST("EXPRESION")
        nodeExp.addChildrenNode(self.condicion.getNode())
        nodeWhile.addChildrenNode(nodeExp)

        nodeInstructions = nodeAST("INSTRUCCIONES")
        for instruccion in self.instrucciones:
            if isinstance(instruccion, Excepcion): continue
            nodeInstructions.addChildrenNode(instruccion.getNode())
        nodeWhile.addChildrenNode(nodeInstructions)
        nodeWhile.addChild("end;")

        return nodeWhile
    
    def interpretar(self, table, tree):
        while(True):
            myCondition = self.condicion.interpretar(table, tree)
            if isinstance(myCondition, Excepcion): return myCondition
            if self.condicion.type != TIPO_DATO.BOOLEANO: return Excepcion("Semantico", "Se esperaba un valor booleano", self.line, self.column)

            if myCondition:
                newTable = Tabla(table)
                globalTable = None
                for instruccion in self.instrucciones:
                    if isinstance(instruccion, Excepcion):
                        tree.updateConsole(instruccion.imprimir())
                        continue
                    if isinstance(instruccion, Return):
                        return instruccion
                    result = None
                    if isinstance(instruccion, If):
                        if globalTable != None:
                            result = instruccion.interpretar(globalTable, tree, 'While')
                        else:
                            result = instruccion.interpretar(newTable, tree, 'While')
                    elif isinstance(instruccion, Global):
                        result = instruccion.interpretar(newTable, tree)
                        globalTable = result
                    else:
                        if globalTable != None:
                            result = instruccion.interpretar(globalTable, tree)
                        else:
                            result = instruccion.interpretar(newTable, tree)
                    if isinstance(result, Excepcion):
                        tree.updateConsole(result.imprimir())
                    if isinstance(result, Return):
                        return result
                    if isinstance(result, Break):
                        return None
                    if isinstance(result, Continue):
                        break
            else:
                break;
        return None

    def getC3D(self, contador):
        return ""