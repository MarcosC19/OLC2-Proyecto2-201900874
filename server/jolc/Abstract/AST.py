from abc import ABC, abstractmethod

class AST(ABC):
    def __init__(self, type, line, column):
        self.type = type
        self.line = line
        self.column = column
        super().__init__()

    @abstractmethod
    def interpretar(self, table, tree):
        pass

    @abstractmethod
    def getNode(self):
        pass

    @abstractmethod
    def getC3D(self):
        pass