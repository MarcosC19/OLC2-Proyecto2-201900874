class Expresion():

    def __init__(self, operador1, operador, operador2):
        self.operador1 = operador1
        self.operator = operador
        self.operador2 = operador2

    def printAsign(self):
        return str(self.operador1) + " " + str(self.operator) + " " + str(self.operador2) + ";\n"