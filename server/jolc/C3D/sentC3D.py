class C3D():

    def __init__(self):
        self.code = ""
        self.contadorT = 0
        self.contadorL = 0

    def addC3D(self, code):
        self.code += code

    def getC3D(self):
        return self.code

    def getContadorT(self):
        return self.contadorT

    def getContadorL(self):
        return self.contadorL

    def addContadorT(self):
        self.contadorT += 1

    def addContadorL(self):
        self.contadorL += 1

    def getLastContadorT(self):
        return self.contadorT - 1

    def getLastContadorL(self):
        return self.contadorL - 1

    def initC3D(self):
        self.code += "package main;\n\n"
        self.code += "import(\n"
        self.code += "   \"fmt\"\n"
        self.code += ")\n\n"
        self.code += "var stack[32000000]float64;\n"
        self.code += "var heap[32000000]float64;\n"
        self.code += "var P, H float64;\n"