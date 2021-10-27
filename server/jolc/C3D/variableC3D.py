from enum import Enum

class VariableC3D():

    def __init__(self, nombre, posicion, tipo, tipoVal):
        self.name = nombre
        self.position = posicion
        self.type = tipo
        self.typeVal = tipoVal

    def getName(self):
        return self.name

    def getPosition(self):
        return self.position

class TipoVar(Enum):
    VALOR = 1,
    APUNTADOR = 2