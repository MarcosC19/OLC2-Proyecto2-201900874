from datetime import datetime


class Excepcion():
    def __init__(self, type, description, file, column):
        self.type = type
        self.description = description
        self.file = file
        self.column = column
        self.time = datetime.today()

    def toString(self):
        return "Error " + str(self.type) + " en [" + str(self.file) + ", " + str(self.column)  + "]" + " - " + str(self.description)

    def imprimir(self):
        return self.toString() + "\n"

    def getType(self):
        return self.type

    def getDesc(self):
        return self.description

    def getFile(self):
        return self.file

    def getColumn(self):
        return self.column

    def getTime(self):
        return self.time