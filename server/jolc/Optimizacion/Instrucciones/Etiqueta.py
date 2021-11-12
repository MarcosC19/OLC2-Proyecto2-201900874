class Etiqueta():

    def __init__(self, nombre, file):
        self.nombre = nombre
        self.fila = file

    def printAsign(self):
        return self.nombre + ":\n"