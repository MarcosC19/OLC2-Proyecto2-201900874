class Arbol():

    def __init__(self, instrucciones):
        self.instructions = instrucciones
        self.exceptions = []
        self.functions = {}
        self.consola = ""
        self.TSglobal = None
        self.contador = 0
        self.dot = ""

    def getInstructions(self):
        return self.instructions

    def setInstructions(self, instrucciones):
        self.instructions = instrucciones
    
    def getExceptions(self):
        return self.exceptions

    def setExceptions(self, excepciones):
        self.exceptions = excepciones

    def getConsole(self):
        return self.consola

    def setConsole(self, consola):
        self.consola = consola

    def updateConsole(self, cadena):
        self.consola += str(cadena)

    def getGlobal(self):
        return self.TSglobal

    def setGlobal(self, table):
        self.TSglobal = table

    def getFunctions(self):
        return self.functions

    def getFunction(self, funcionN):
        if funcionN.identificador in self.functions:
            return self.functions[funcionN.identificador]
        return None

    def addFunctions(self, funcion):
        if funcion.identificador not in self.functions:
            self.functions[funcion.identificador] = funcion
        return None

    def getDot(self, raiz):
        self.dot = ""
        self.dot += "charset=\"latin1\"\n"
        self.dot += "n0[label=\"" + raiz.getValue().replace("\"", "\\\"") + "\"];\n"
        self.contador += 1
        self.recorrerAST("n0", raiz)
        return self.dot

    def recorrerAST(self, padre, nPadre):
        for hijo in nPadre.getChildren():
            nombreHijo = "n" + str(self.contador)
            self.dot += nombreHijo + "[label=\"" + hijo.getValue().replace("\"", "\\\"") + "\"];\n"
            self.dot += padre + "->" + nombreHijo + ";\n"
            self.contador += 1
            self.recorrerAST(nombreHijo, hijo)