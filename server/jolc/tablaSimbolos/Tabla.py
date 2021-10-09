from Excepciones.Excepcion import Excepcion

class Tabla():

    def __init__(self, anterior = None):
        self.anterior = anterior
        self.tabla = {}

    def setVariable(self, simbolo):
        self.tabla[simbolo.getId()] = simbolo
        return None
        
    def getVariable(self, identificador):
        tablaActual = self
        while tablaActual != None:
            if identificador in tablaActual.tabla:
                return tablaActual.tabla[identificador]
            else:
                tablaActual = tablaActual.anterior
        return None