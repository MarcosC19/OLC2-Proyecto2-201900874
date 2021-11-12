class If():

    def __init__(self, expresion, salto, file):
        self.expresion = expresion
        self.salto = salto
        self.fila = file

    def printAsign(self):
        return "if "+ str(self.expresion.printAsign()) + "{ " + str(self.salto.printAsign()) + " }\n"