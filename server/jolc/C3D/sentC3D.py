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

    def addPrintString(self):
        codePrint = "func printString(){\n"
        codePrint += "  t" + str(self.getContadorT()) + " = P + 1;\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        codePrint += "  t" + str(self.getContadorT()) + " = stack[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT2 = self.getContadorT()
        self.addContadorT()
        printCode = "      t" + str(self.getContadorT()) + " = heap[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        printCode += "      if t" + str(temporalT3) + " == -1 { goto L" +  str(self.getContadorL()) + "; }\n"
        temporalL1 = self.getContadorL() # dfag
        self.addContadorL()
        printCode += "      fmt.Printf(\"%c\", int(t" + str(temporalT3) + "));\n"
        printCode += "      t" + str(temporalT2) + " = t" + str(temporalT2) + " + 1;\n"
        printCode += "      goto L" + str(self.getContadorL()) + ";\n"
        temporalL2 = self.getContadorL() # dfag
        self.addContadorL()
        printCode += "      L" + str(temporalL1) + ":\n"
        printCode += "          return;"
        codePrint += "  L" + str(temporalL2) + ":\n"
        codePrint += printCode + "\n"
        codePrint += "}\n\n"
        return codePrint

    def addPotencia(self):
        codePot = "func potenciaM(){\n"
        codePot += "    t" + str(self.getContadorT()) + " = P + 2;\n"
        temporalT0 = self.getContadorT()
        self.addContadorT()
        codePot += "    t" + str(self.getContadorT()) + " = P + 0;\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        codePot += "    t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalT1) + ")];\n"
        temporalT2 = self.getContadorT()
        self.addContadorT()
        codePot += "    stack[int(t" + str(temporalT0) + ")] = t" + str(temporalT2) + ";\n"

        enterPot = "        t" + str(self.getContadorT()) + " = P + 1;\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        enterPot += "       t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalT3) + ")];\n"
        temporalT4 = self.getContadorT()
        self.addContadorT()
        enterPot += "       if t" + str(temporalT4) + " > 1 { goto L" + str(self.getContadorL()) + "; }\n"
        temporalL0 = self.getContadorL()
        self.addContadorL()
        enterPot += "       goto L" + str(self.getContadorL()) + ";\n"
        temporalL1 = self.getContadorL()
        self.addContadorL()
        enterPot += "       L" + str(temporalL0) + ":\n"
        enterPot += "           t" + str(self.getContadorT()) + " = P + 2;\n"
        temporalT5 = self.getContadorT()
        self.addContadorT()
        enterPot += "           t" + str(self.getContadorT()) + " = P + 2;\n"
        temporalT6 = self.getContadorT()
        self.addContadorT()
        enterPot += "           t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalT6) + ")];\n"
        temporalT7 = self.getContadorT()
        self.addContadorT()
        enterPot += "           t" + str(self.getContadorT()) + " = P + 0;\n"
        temporalT8 = self.getContadorT()
        self.addContadorT()
        enterPot += "           t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalT8) + ")];\n"
        temporalT9 = self.getContadorT()
        self.addContadorT()
        enterPot += "           t" + str(self.getContadorT()) + " = t" + str(temporalT7) + " * t" + str(temporalT9) + ";\n"
        temporalT10 = self.getContadorT()
        self.addContadorT()
        enterPot += "           stack[int(t" + str(temporalT5) + ")] = t" + str(temporalT10) + ";\n"
        enterPot += "           t" + str(self.getContadorT()) + " = P + 1;\n"
        temporalT11 = self.getContadorT()
        self.addContadorT()
        enterPot += "           t" + str(self.getContadorT()) + " = P + 1;\n"
        temporalT12 = self.getContadorT()
        self.addContadorT()
        enterPot += "           t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalT12) + ")];\n"
        temporalT13 = self.getContadorT()
        self.addContadorT()
        enterPot += "           t" + str(self.getContadorT()) + " = t" + str(temporalT13) + " - 1;\n"
        temporalT14 = self.getContadorT()
        self.addContadorT()
        enterPot += "           stack[int(t" + str(temporalT11) + ")] = t" + str(temporalT14) + ";\n"
        enterPot += "           goto L" + str(self.getContadorL()) + ";\n"
        temporalL2 = self.getContadorL()
        self.addContadorL()

        codePot += "    L" + str(temporalL2) + ":\n"
        codePot += enterPot
        codePot += "    L" + str(temporalL1) + ":\n"

        codePot += "        if t" + str(temporalT4) + " == 0 { goto L" + str(self.getContadorL()) + "; }\n"
        temporalL4 = self.getContadorL()
        self.addContadorL()
        codePot += "        goto L" + str(self.getContadorL()) + ";\n"
        temporalL5 = self.getContadorL()
        self.addContadorL()

        codePot += "        L" + str(temporalL4) + ":\n"
        codePot += "            t" + str(self.getContadorT()) + " = P + 3;\n"
        temporalT18 = self.getContadorT()
        self.addContadorT()
        codePot += "            stack[int(t" + str(temporalT18) + ")] = 1;\n"
        codePot += "            return;\n"
        codePot += "    L" + str(temporalL5) + ":\n"

        codePot += "    t" + str(self.getContadorT()) + " = P + 3;\n"
        temporalT15 = self.getContadorT()
        self.addContadorT()
        codePot += "    t" + str(self.getContadorT()) + " = P + 2;\n"
        temporalT16 = self.getContadorT()
        self.addContadorT()
        codePot += "    t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalT16) + ")];\n"
        temporalT17 = self.getContadorT()
        self.addContadorT()
        codePot += "    stack[int(t" + str(temporalT15) + ")] = t" + str(temporalT17) + ";\n"
        codePot += "    goto L" + str(self.getContadorL()) + ";\n"
        temporalL3 = self.getContadorL()
        self.addContadorL()
        codePot += "    L" + str(temporalL3) + ":\n"
        codePot += "        return;\n"

        codePot += "}\n\n"
        return codePot

    def printTrue(self):
        C3D = ""
        for i in 'true':
            C3D += "    fmt.Printf(\"%c\", " + str(ord(i)) + ");\n"
        return C3D

    def printFalse(self):
        C3D = ""
        for i in 'false':
            C3D += "    fmt.Printf(\"%c\", " + str(ord(i)) + ");\n"
        return C3D

    def initC3D(self):
        self.code += "package main;\n\n"
        self.code += "import(\n"
        self.code += "   \"fmt\"\n"
        self.code += ")\n\n"
        self.code += "var stack[32000000]float64;\n"
        self.code += "var heap[32000000]float64;\n"
        self.code += "var P, H float64;\n"