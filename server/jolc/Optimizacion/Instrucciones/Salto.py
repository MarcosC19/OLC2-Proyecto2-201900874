class Salto():

    def __init__(self, etiqueta, file):
        self.etiqueta = etiqueta
        self.fila = file

    def printAsign(self):
        return "goto " + str(self.etiqueta) + ";\n"