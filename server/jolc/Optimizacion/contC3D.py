from enum import Enum

from .Instrucciones.Asignacion import Asignacion

class contC3D():

    def __init__(self, encabezado, funciones):
        self.encabezado = encabezado
        self.funciones = funciones
        self.reporteOpt = []

    def OptMirilla(self):
        print("optimizando")
        newCode = self.encabezado
        newFunction = ""
        contadorR1 = 0
        for funcion in self.funciones:
            newFunction += "func " + str(funcion.nombre) + "(){\n"
            
            instruccionNew = ""
            # REGLA 1
            for instruccion in funcion.instrucciones:
                instruccionNew = instruccion.printAsign()
                for instruccion2 in funcion.instrucciones:
                    if instruccion2 != instruccion:
                        if isinstance(instruccion, Asignacion) and isinstance(instruccion2, Asignacion):
                            
                            if instruccion.identificador == instruccion2.expresion:
                                contadorR1 += 1
                            if instruccion.expresion == instruccion2.identificador:
                                contadorR1 += 1

                if contadorR1 == 2:
                    instruccionNew += ""

                newFunction += instruccionNew
                contadorR1 = 0

            # REGLA 2
            newFunction += "}\n\n"
            newCode += newFunction
            newFunction = ""
        return newCode

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

class TipoOOPT(Enum):
    MIRILLA = 0,
    BLOQUEG = 1,
    BLOQUEL = 2