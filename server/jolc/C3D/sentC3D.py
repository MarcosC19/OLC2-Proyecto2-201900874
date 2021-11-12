import re


class C3DT():

    def __init__(self):
        self.code = ""
        self.contadorT = 0
        self.contadorL = 0
        self.numVariablesG = 0
        self.variables = {}
        self.funciones = {}
        self.mathCont = 0

    def addFunction(self, nombre, funcion):
        self.funciones[nombre] = funcion

    def getFunction(self, nombre):
        if nombre in self.funciones:
            return self.funciones[nombre]
        return None

    def addC3D(self, code):
        self.code += code

    def addVariable(self, nombre, variable):
        self.variables[nombre] = variable

    def getVariable(self, nombre):
        if nombre in self.variables:
            return self.variables[nombre]
        return None

    def getC3D(self):
        return self.code

    def getContadorT(self):
        return self.contadorT

    def getContadorL(self):
        return self.contadorL

    def getNumVariables(self):
        return self.numVariablesG

    def addNumVariable(self):
        self.numVariablesG += 1

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
        codePrint += "  t" + str(self.getContadorT()) + " = P + 0;\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        codePrint += "  t" + str(self.getContadorT()) + " = stack[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT2 = self.getContadorT()
        self.addContadorT()
        printCode = "      t" + str(self.getContadorT()) + " = heap[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        printCode += "      if t" + str(temporalT3) + " == -1 { goto L" +  str(self.getContadorL()) + "; }\n"
        temporalL1 = self.getContadorL()
        self.addContadorL()
        printCode += "      fmt.Printf(\"%c\", int(t" + str(temporalT3) + "));\n"
        printCode += "      t" + str(temporalT2) + " = t" + str(temporalT2) + " + 1;\n"
        printCode += "      goto L" + str(self.getContadorL()) + ";\n"
        temporalL2 = self.getContadorL()
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

    def addPrintList(self):
        codePrint = "func printList(){\n"
        codePrint += "  t" + str(self.getContadorT()) + " = P + 0;\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        codePrint += "  t" + str(self.getContadorT()) + " = stack[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT2 = self.getContadorT()
        self.addContadorT()
        printCode = "      t" + str(self.getContadorT()) + " = heap[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        printCode += "      if t" + str(temporalT3) + " == -1 { goto L" +  str(self.getContadorL()) + "; }\n"
        temporalL1 = self.getContadorL()
        self.addContadorL()
        printCode += "      fmt.Printf(\"%f \", t" + str(temporalT3) + ");\n"
        printCode += "      t" + str(temporalT2) + " = t" + str(temporalT2) + " + 1;\n"
        printCode += "      goto L" + str(self.getContadorL()) + ";\n"
        temporalL2 = self.getContadorL()
        self.addContadorL()
        printCode += "      L" + str(temporalL1) + ":\n"
        printCode += "          return;"
        codePrint += "  L" + str(temporalL2) + ":\n"
        codePrint += printCode + "\n"
        codePrint += "}\n\n"
        return codePrint

    def addUpper(self):
        codePrint = "func upperCase(){\n"

        codePrint += "  t" + str(self.getContadorT()) + " = P + 0;\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        codePrint += "  t" + str(self.getContadorT()) + " = stack[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT2 = self.getContadorT()
        self.addContadorT()
        printCode = "      t" + str(self.getContadorT()) + " = heap[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        printCode += "      if t" + str(temporalT3) + " == -1 { goto L" +  str(self.getContadorL()) + "; }\n"
        temporalL1 = self.getContadorL()
        self.addContadorL()
        printCode += "      if t" + str(temporalT3) + " < 97 { goto L" + str(self.getContadorL()) + "; }\n"
        printCode += "      if t" + str(temporalT3) + " > 123 { goto L" + str(self.getContadorL()) + "; }\n"
        temporalL10 = self.getContadorL()
        self.addContadorL()

        printCode += "      t" + str(temporalT3) + " = t" + str(temporalT3) + " - 32;\n"
        printCode += "      L" + str(temporalL10) + ":\n"
        printCode += "      heap[int(H)] = t" + str(temporalT3) + ";\n"
        printCode += "      H = H + 1;\n"
        printCode += "      t" + str(temporalT2) + " = t" + str(temporalT2) + " + 1;\n"
        printCode += "      goto L" + str(self.getContadorL()) + ";\n"
        temporalL2 = self.getContadorL()
        self.addContadorL()
        printCode += "      L" + str(temporalL1) + ":\n"
        printCode += "          return;"
        codePrint += "  L" + str(temporalL2) + ":\n"
        codePrint += printCode + "\n"
        
        codePrint += "}\n\n"
        return codePrint

    def addLower(self):
        codePrint = "func lowerCase(){\n"

        codePrint += "  t" + str(self.getContadorT()) + " = P + 0;\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        codePrint += "  t" + str(self.getContadorT()) + " = stack[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT2 = self.getContadorT()
        self.addContadorT()
        printCode = "      t" + str(self.getContadorT()) + " = heap[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        printCode += "      if t" + str(temporalT3) + " == -1 { goto L" +  str(self.getContadorL()) + "; }\n"
        temporalL1 = self.getContadorL()
        self.addContadorL()
        printCode += "      if t" + str(temporalT3) + " < 65 { goto L" + str(self.getContadorL()) + "; }\n"
        printCode += "      if t" + str(temporalT3) + " > 91 { goto L" + str(self.getContadorL()) + "; }\n"
        temporalL10 = self.getContadorL()
        self.addContadorL()

        printCode += "      t" + str(temporalT3) + " = t" + str(temporalT3) + " + 32;\n"
        printCode += "      L" + str(temporalL10) + ":\n"
        printCode += "      heap[int(H)] = t" + str(temporalT3) + ";\n"
        printCode += "      H = H + 1;\n"
        printCode += "      t" + str(temporalT2) + " = t" + str(temporalT2) + " + 1;\n"
        printCode += "      goto L" + str(self.getContadorL()) + ";\n"
        temporalL2 = self.getContadorL()
        self.addContadorL()
        printCode += "      L" + str(temporalL1) + ":\n"
        printCode += "          return;"
        codePrint += "  L" + str(temporalL2) + ":\n"
        codePrint += printCode + "\n"
        
        codePrint += "}\n\n"
        return codePrint

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

    def printMathError(self, resultado2C3D):
        C3D = "    /* COMPROBACION DINAMICA MATH-ERROR */\n"
        if isinstance(resultado2C3D, list):
            for texto in resultado2C3D:
                C3D += "    if " + str(texto) + " != 0 { goto L" + str(self.getContadorL()) + ";}\n"
            temporalL0 = self.getContadorL()
            self.addContadorL()
        else:
            C3D += "    if t" + str(resultado2C3D) + " != 0 { goto L" + str(self.getContadorL()) + ";}\n"
            temporalL0 = self.getContadorL()
            self.addContadorL()
        for i in 'MathError':
            C3D += "    fmt.Printf(\"%c\", " + str(ord(i)) + ");\n"
        C3D += "    fmt.Printf(\"%c\\n\", 32);\n"
        C3D += "    t" + str(self.getContadorT()) + " = 0;\n"
        C3D += "    goto L" + str(self.getContadorL()) + ";\n"
        temporalL1 = self.getContadorL()
        return C3D

    def saveString(self, cadena):
        C3D = "    /* GUARDANDO STRING */\n"
        C3D += "    t" + str(self.getContadorT()) + " = H;\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        for i in cadena:
            C3D += "    heap[int(H)] = " + str(ord(i)) + ";\n"
            C3D += "    H = H + 1;\n"
        return C3D

    def chargeTrue(self):
        C3D = ""
        C3D += self.saveString("true")
        C3D += self.endString()
        return C3D

    def endString(self):
        C3D = "    /* CERRANDO CADENA */\n"
        C3D += "    heap[int(H)] = -1;\n"
        C3D += "    H = H + 1;\n"
        return C3D

    def printString(self, contador):
        C3D = "    /* IMPRIMIENDO STRING */\n"
        C3D += "    t" + str(self.getContadorT()) + " = P + " + str(self.getNumVariables()) + ";\n"
        temporalT1 = self.getLastContadorT()
        temporalT2 = self.getContadorT()
        self.addContadorT()
        C3D += "    t" + str(self.getContadorT()) + " = t" + str(temporalT2) + " + 0;\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        C3D += "    stack[int(t" + str(temporalT3) + ")] = t" + str(contador) + ";\n"
        C3D += "    P = P + " + str(self.getNumVariables()) + ";\n"
        C3D += "    printString();\n"
        C3D += "    t" + str(self.getContadorT()) + " = stack[int(P)];\n"
        C3D += "    P = P - " + str(self.getNumVariables()) + ";\n"
        return C3D

    def printUpper(self, contador):
        C3D = "    /* UPPERCASE STRING */\n"
        C3D += "    t" + str(self.getContadorT()) + " = P + " + str(self.getNumVariables()) + ";\n"
        temporalT1 = self.getLastContadorT()
        temporalT2 = self.getContadorT()
        self.addContadorT()
        C3D += "    t" + str(self.getContadorT()) + " = t" + str(temporalT2) + " + 0;\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        C3D += "    stack[int(t" + str(temporalT3) + ")] = t" + str(contador) + ";\n"
        C3D += "    P = P + " + str(self.getNumVariables()) + ";\n"
        C3D += "    upperCase();\n"
        C3D += "    t" + str(self.getContadorT()) + " = stack[int(P)];\n"
        C3D += "    P = P - " + str(self.getNumVariables()) + ";\n"
        return C3D

    def printLower(self, contador):
        C3D = "    /* LOWERCASE STRING */\n"
        C3D += "    t" + str(self.getContadorT()) + " = P + " + str(self.getNumVariables()) + ";\n"
        temporalT1 = self.getLastContadorT()
        temporalT2 = self.getContadorT()
        self.addContadorT()
        C3D += "    t" + str(self.getContadorT()) + " = t" + str(temporalT2) + " + 0;\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        C3D += "    stack[int(t" + str(temporalT3) + ")] = t" + str(contador) + ";\n"
        C3D += "    P = P + " + str(self.getNumVariables()) + ";\n"
        C3D += "    lowerCase();\n"
        C3D += "    t" + str(self.getContadorT()) + " = stack[int(P)];\n"
        C3D += "    P = P - " + str(self.getNumVariables()) + ";\n"
        return C3D

    def printList(self, contador):
        C3D = "    /* IMPRIMIENDO STRING */\n"
        C3D += "    t" + str(self.getContadorT()) + " = P + " + str(self.getNumVariables()) + ";\n"
        temporalT1 = self.getLastContadorT()
        temporalT2 = self.getContadorT()
        self.addContadorT()
        C3D += "    t" + str(self.getContadorT()) + " = t" + str(temporalT2) + " + 0;\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        C3D += "    stack[int(t" + str(temporalT3) + ")] = t" + str(contador) + ";\n"
        C3D += "    P = P + " + str(self.getNumVariables()) + ";\n"
        C3D += "    printList();\n"
        C3D += "    t" + str(self.getContadorT()) + " = stack[int(P)];\n"
        C3D += "    P = P - " + str(self.getNumVariables()) + ";\n"
        return C3D
    
    def changePot(self):
        C3D = ""
        C3D += "    P = P + " + str(self.getNumVariables()) + ";\n"
        C3D += "    potenciaM();\n"
        C3D += "    t" + str(self.getContadorT()) + " = P + 3;\n"
        temporalAux4 = self.getContadorT()
        self.addContadorT()
        C3D += "    t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalAux4) + ")];\n"
        self.addContadorT()
        C3D += "    P = P - " + str(self.getNumVariables()) + ";\n"
        return C3D

    def addCompareString(self):
        C3D = "func compareString(){\n"
        C3D += "    t" + str(self.getContadorT()) + " = P + 0;\n"
        temporalT0 = self.getContadorT()
        self.addContadorT()
        C3D += "    t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalT0) + ")];\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        C3D += "    t" + str(self.getContadorT()) + " = P + 1;\n"
        temporalT2 = self.getContadorT()
        self.addContadorT()
        C3D += "    t" + str(self.getContadorT()) + " = stack[int(t" + str(temporalT2) + ")];\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()

        codeFor = "        t" + str(self.getContadorT()) + " = heap[int(t" + str(temporalT1) + ")];\n"
        temporalT4 = self.getContadorT()
        self.addContadorT()
        codeFor += "        t" + str(self.getContadorT()) + " = heap[int(t" + str(temporalT3) + ")];\n"
        temporalT5 = self.getContadorT()
        self.addContadorT()
        codeFor += "        if t" + str(temporalT4) + " == t" + str(temporalT5) + " { goto L" + str(self.getContadorL()) + "; }\n"
        temporalL0 = self.getContadorL()
        self.addContadorL()
        codeFor += "        goto L" + str(self.getContadorL()) + ";\n"
        temporalL1 = self.getContadorL()
        self.addContadorL()
        codeFor += "        L" + str(temporalL0) + ":\n"
        codeFor += "            if t" + str(temporalT4) + " == -1 { goto L" + str(self.getContadorL()) + "; }\n"
        temporaL2 = self.getContadorL()
        self.addContadorL()
        codeFor += "            t" + str(temporalT1) + " = t" + str(temporalT1) + " + 1;\n"
        codeFor += "            L" + str(temporaL2) + ":\n"
        codeFor += "                if t" + str(temporalT5) + " == -1 { goto L" + str(self.getContadorL()) + "; }\n"
        temporalL3 = self.getContadorL()
        self.addContadorL()
        codeFor += "                t" + str(temporalT3) + " = t" + str(temporalT3) + " + 1;\n"
        codeFor += "                goto L" + str(self.getContadorL()) + ";\n"
        temporalL4 = self.getContadorL()
        self.addContadorL()

        C3D += "    L" + str(temporalL4) + ":\n"
        C3D += codeFor
        C3D += "    L" + str(temporalL1) + ":\n"
        C3D += "        t" + str(self.getContadorT()) + " = P + 2;\n"
        temporalT6 = self.getContadorT()
        self.addContadorT()
        C3D += "        stack[int(t" + str(temporalT6) + ")] = 0;\n"
        C3D += "        return;\n"
        C3D += "    L" + str(temporalL3) + ":\n"
        C3D += "        t" + str(self.getContadorT()) + " = P + 2;\n"
        temporalT7 = self.getContadorT()
        self.addContadorT()
        C3D += "        stack[int(t" + str(temporalT7) + ")] = 1;\n"
        C3D += "        return;\n"
        C3D += "}\n\n"
        return C3D
    
    def initC3D(self):
        self.code += "package main;\n\n"
        self.code += "import(\n"
        self.code += "    \"fmt\""

    def addLastIMP(self):
        self.code += "\n)\n\n"
        self.code += "var stack[32000000]float64;\n"
        self.code += "var heap[32000000]float64;\n"
        self.code += "var P, H float64;\n"

    def addMath(self):
        self.code += ";\n    \"math\""
        self.mathCont += 1

    def printBoundsError(self, position, limiteS):
        C3D = "    /* COMPROBACION DINAMICA BOUNDS-ERROR*/\n"
        C3D += "    t" + str(self.getContadorT()) + " = " + str(position) + ";\n"
        C3D += "    if t" + str(self.getContadorT()) + " < 1 { goto L" + str(self.getContadorL()) + "; }\n"
        C3D += "    if t" + str(self.getContadorT()) + " > " + str(limiteS) +" { goto L" + str(self.getContadorL()) + "; }\n"
        temporalErr = self.getContadorL()
        self.addContadorL()
        C3D += "    goto L" + str(self.getContadorL()) + ";\n"
        temporalB = self.getContadorL()
        self.addContadorL()
        C3D += "    L" + str(temporalErr) + ":\n"
        C3D += "    fmt.Printf(\"%c\", 66);\n"
        C3D += "    fmt.Printf(\"%c\", 111);\n"
        C3D += "    fmt.Printf(\"%c\", 117);\n"
        C3D += "    fmt.Printf(\"%c\", 110);\n"
        C3D += "    fmt.Printf(\"%c\", 100);\n"
        C3D += "    fmt.Printf(\"%c\", 115);\n"
        C3D += "    fmt.Printf(\"%c\", 69);\n"
        C3D += "    fmt.Printf(\"%c\", 114);\n"
        C3D += "    fmt.Printf(\"%c\", 114);\n"
        C3D += "    fmt.Printf(\"%c\", 111);\n"
        C3D += "    fmt.Printf(\"%c\\n\", 114);\n"
        C3D += "    goto L" + str(self.getContadorL()) + ";\n"
        temporalN = self.getContadorL()
        self.addContadorL()
        C3D += "    L" + str(temporalB) + ":\n"

        self.addContadorT()
        return [C3D, temporalN]

    def addLength(self):
        C3D = "func getLength(){\n"

        C3D += "    t" + str(self.getContadorT()) + " = 0;\n"
        contadorR = self.getContadorT()
        self.addContadorT()

        codePrint = "    t" + str(self.getContadorT()) + " = P + 0;\n"
        temporalT1 = self.getContadorT()
        self.addContadorT()
        codePrint += "    t" + str(self.getContadorT()) + " = stack[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT2 = self.getContadorT()
        self.addContadorT()
        printCode = "      t" + str(self.getContadorT()) + " = heap[int(t" + str(self.getLastContadorT()) + ")];\n"
        temporalT3 = self.getContadorT()
        self.addContadorT()
        printCode += "      if t" + str(temporalT3) + " == -1 { goto L" +  str(self.getContadorL()) + "; }\n"
        temporalL1 = self.getContadorL()
        self.addContadorL()
        printCode += "      t" + str(temporalT2) + " = t" + str(temporalT2) + " + 1;\n"
        printCode += "      t" + str(contadorR) + " = t" + str(contadorR) + " + 1;\n"
        printCode += "      goto L" + str(self.getContadorL()) + ";\n"
        temporalL2 = self.getContadorL()
        self.addContadorL()
        printCode += "      L" + str(temporalL1) + ":\n"
        printCode += "      t" + str(self.getContadorT()) + " = P + 1;\n"
        otroC = self.getContadorT()
        self.addContadorT()
        printCode += "          stack[int(t" + str(otroC) + ")] = t" + str(contadorR) + ";\n"
        printCode += "          return;"
        codePrint += "    L" + str(temporalL2) + ":\n"
        codePrint += printCode + "\n"

        C3D += codePrint + "\n"
        C3D += "}\n\n"
        return C3D