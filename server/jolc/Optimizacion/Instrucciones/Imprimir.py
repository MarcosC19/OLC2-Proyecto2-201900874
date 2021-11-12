class Imprimir():

    def __init__(self, tipo, expresion, file):
        self.tipo = tipo
        self.expresion = expresion
        self.fila = file
    
    def printAsign(self):
        return "fmt.Printf(\"" + str(self.tipo) + "\", "+ str(self.expresion)  +");\n"