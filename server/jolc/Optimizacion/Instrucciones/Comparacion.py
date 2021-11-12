class Comparacion():

    def __init__(self, parte1, signo, parte2, file):
        self.operating1 = parte1
        self.operator = signo
        self.operating2 = parte2
        self.fila = file

    def printAsign(self):
        return str(self.operating1) + self.operator + str(self.operating2)