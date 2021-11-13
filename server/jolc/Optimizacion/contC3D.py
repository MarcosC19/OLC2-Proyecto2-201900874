from enum import Enum

from .Instrucciones.Expresion import Expresion
from .Instrucciones.Etiqueta import Etiqueta
from .Instrucciones.Salto import Salto
from .Instrucciones.Asignacion import Asignacion
from .Reporte.reporte import Reporte

class contC3D():

    def __init__(self, encabezado, funciones):
        self.encabezado = encabezado
        self.funciones = funciones
        self.reporteOpt = []

    def OptMirilla(self):
        newCode = self.encabezado
        newFunction = ""
        contadorR1 = 0
        reportes = []
        for funcion in self.funciones:
            newFunction += "func " + str(funcion.nombre) + "(){\n"
            instruccionNew = ""
            for instruccion in funcion.instrucciones:
                instruccionNew = instruccion.printAsign()

                regla1 = self.Regla1(funcion.instrucciones, instruccion, contadorR1, reportes)
                regla2 = self.Regla2(funcion.instrucciones, instruccion, reportes)
                regla6 = self.Regla6(instruccion, reportes)
                regla7 = self.Regla7(instruccion, reportes)
                regla8 = self.Regla8(instruccion, reportes)

                if regla1[1]:
                    newFunction += regla1[0]
                elif regla2[1]:
                    newFunction += regla2[0]
                elif regla6:
                    newFunction += ""
                elif regla7[1]:
                    newFunction += regla7[0]
                elif regla8[1]:
                    newFunction += regla8[0]
                else:
                    newFunction += instruccionNew
            
            newFunction += "}\n"
            newCode += newFunction
            newFunction = ""
        return [newCode, reportes]

    def Regla1(self, listado, instruccion, contadorR1, reportes):
        newFunction = ""
        isAplicable = False
        for instruccion2 in listado:
            if instruccion2 != instruccion:
                if isinstance(instruccion, Asignacion) and isinstance(instruccion2, Asignacion):
                    # REGLA 1
                    if instruccion.identificador == instruccion2.expresion:
                        contadorR1 += 1
                        if instruccion.expresion == instruccion2.identificador:
                            isAplicable = True
                            nuevoR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA1, instruccion.printAsign() + "\n" + instruccion2.printAsign(), instruccion.printAsign(), instruccion.fila)
                            reportes.append(nuevoR)
                            listado.remove(instruccion2)
                            newFunction += instruccion.printAsign()
        return [newFunction, isAplicable]

    def Regla2(self, listado, instruccion, reportes):
        newFunction = ""
        isAplicable = False
        instrucciones = []
        backINS = ""
        expresionAnti = ""
        for instruccion2 in listado:

            if listado.index(instruccion) < listado.index(instruccion2):
                if isinstance(instruccion, Salto):
                    newFunction = instruccion.printAsign()
                    if not isinstance(instruccion2, Etiqueta):
                        backINS += instruccion2.printAsign()
                        instrucciones.append(listado.index(instruccion2)) 
                    else:
                        if instruccion2.nombre == instruccion.etiqueta:
                            expresionAnti += newFunction
                            expresionAnti += backINS
                            expresionAnti += instruccion2.printAsign()
                            
                            newFunction += instruccion2.printAsign()
                            instrucciones.append(listado.index(instruccion2))
                            isAplicable = True
                            newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA2, expresionAnti, newFunction, instruccion.fila)
                            reportes.append(newR)
                            break
                        else:
                            isAplicable = False
                            newFunction = instruccion.printAsign()
                            break
        if isAplicable:
            instrucciones.reverse()
            for eliminar in instrucciones:
                listado.pop(eliminar)

        return [newFunction, isAplicable]
        

    def Regla6(self, instruccion, reportes):
        isAplicable = False
        if isinstance(instruccion, Asignacion):
            identifier = instruccion.identificador
            expresion = instruccion.expresion
            if isinstance(expresion, Expresion):
                operador1 = expresion.operador1
                operator = expresion.operator
                operador2 = expresion.operador2
                if identifier == operador1:
                    if operator == "+" or operator == "-":
                        if operador2 == 0:
                            isAplicable = True
                            newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA6, instruccion.printAsign(), "Se eliminó la expresión", instruccion.fila)
                            reportes.append(newR)
                    elif operator == "*" or operator == "/":
                        if operador2 == 1:
                            isAplicable = True
                            newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA6, instruccion.printAsign(), "Se eliminó la expresión", instruccion.fila)
                            reportes.append(newR)
        return isAplicable

    def Regla7(self, instruccion, reportes):
        isAplicable = False
        textR = ""
        if isinstance(instruccion, Asignacion):
            identifier = instruccion.identificador
            expresion = instruccion.expresion
            if isinstance(expresion, Expresion):
                operador1 = expresion.operador1
                operator = expresion.operator
                operador2 = expresion.operador2
                if operator == "+" or operator == "-":
                    if operador2 == 0:
                        isAplicable = True
                        textR = identifier + " = " + str(operador1) + ";\n"
                        newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA7, instruccion.printAsign(), textR, instruccion.fila)
                        reportes.append(newR)
                elif operator == "*" or operator == "/":
                    if operador2 == 1:
                        isAplicable = True
                        textR = identifier + " = " + str(operador1) + ";\n"
                        newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA7, instruccion.printAsign(), textR, instruccion.fila)
                        reportes.append(newR)
        return [textR, isAplicable]

    def Regla8(self, instruccion, reportes):
        isAplicable = False
        textR = ""
        if isinstance(instruccion, Asignacion):
            identifier = instruccion.identificador
            expresion = instruccion.expresion
            if isinstance(expresion, Expresion):
                operador1 = expresion.operador1
                operator = expresion.operator
                operador2 = expresion.operador2
                if operator == "*":
                    if operador2 == 2 and isinstance(operador1, str):
                        isAplicable = True
                        textR = identifier + " = " + str(operador1) + " + " + str(operador1) + ";\n"
                        newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA8, instruccion.printAsign(), textR, instruccion.fila)
                        reportes.append(newR)
                    elif operador1 == 2 and isinstance(operador2, str):
                        isAplicable = True
                        textR = identifier + " = " + str(operador2) + " + " + str(operador2) + ";\n"
                        newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA8, instruccion.printAsign(), textR, instruccion.fila)
                        reportes.append(newR)
                    elif (operador1 == 0 and isinstance(operador2, str)) or (operador2 == 0 and isinstance(operador1, str)):
                        isAplicable = True
                        textR = identifier + " = 0;\n"
                        newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA8, instruccion.printAsign(), textR, instruccion.fila)
                        reportes.append(newR)
                elif operator == "/":
                    if (operador1 == 0 and isinstance(operador2, str)):
                        isAplicable = True
                        textR = identifier + " = 0;\n"
                        newR = Reporte(TipoOPT.MIRILLA, ReglasMir.REGLA8, instruccion.printAsign(), textR, instruccion.fila)
                        reportes.append(newR)

        return [textR, isAplicable]
    
    def OptBloque(self):
        print("optimizando")


class ReglasMir(Enum):
    REGLA1 = 0,
    REGLA2 = 1,
    REGLA3 = 2,
    REGLA4 = 3,
    REGLA5 = 4,
    REGLA6 = 5,
    REGLA7 = 6,
    REGLA8 = 7
    

class ReglasBlock(Enum):
    REGLA1 = 0,
    REGLA2 = 1,
    REGLA3 = 2,
    REGLA4 = 3

class TipoOPT(Enum):
    MIRILLA = 0,
    BLOQUEG = 1,
    BLOQUEL = 2