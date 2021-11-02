from enum import Enum

class VariableC3D():

    def __init__(self, nombre, posicion, tipo, tipoVal, tipoVar):
        self.name = nombre
        self.position = posicion
        self.type = tipo
        self.typeVal = tipoVal
        self.typeVariable = tipoVar
        self.tamanios = []

    def getName(self):
        return self.name

    def getPosition(self):
        return self.position

    def getType(self):
        return self.type

    def getTypeVal(self):
        return self.typeVal

    def getTypeVariable(self):
        return self.typeVariable

    def setTam(self, newTam):
        self.tamanios = newTam

    def getTam(self):
        return self.tamanios.copy()

class TipoVar(Enum):
    VALOR = 1,
    APUNTADOR = 2

class TipoVariable(Enum):
    VARIABLE = 1,
    LISTA = 2,
    STRUCT = 3