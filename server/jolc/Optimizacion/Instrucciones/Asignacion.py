from .Expresion import Expresion


class Asignacion():

    def __init__(self, identificador, expresion, file):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = file

    def printAsign(self):
        if isinstance(self.expresion, Expresion):
            return self.identificador + " = " + str(self.expresion.printAsign())
        else:
            return self.identificador + " = " + str(self.expresion) + ";\n"