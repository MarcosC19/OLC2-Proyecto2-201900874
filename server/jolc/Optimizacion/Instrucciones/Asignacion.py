class Asignacion():

    def __init__(self, identificador, expresion, file):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = file

    def printAsign(self):
        return self.identificador + " = " + str(self.expresion) + ";\n"