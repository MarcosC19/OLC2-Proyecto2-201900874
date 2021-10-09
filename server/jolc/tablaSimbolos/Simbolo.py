class Simbolo():
    def __init__(self, type, id, file, column, value):
        self.type = type
        self.id = id
        self.file = file
        self.column = column
        self. value = value
    
    def setId(self, id):
        self.id = id

    def setTipo(self, type):
        self.type = type

    def setValor(self, value):
        self.value = value

    def getId(self):
        return self.id
    
    def getTipo(self):
        return self.type

    def getValor(self):
        return self.value

    def getFile(self):
        return self.file

    def getColumn(self):
        return self.column