class nodeAST():
    def __init__(self, value):
        self.children = []
        self.value = value
    
    def setChildren(self, children = []):
        self.children = children

    def addChild(self, valueChild):
        self.children.append(nodeAST(valueChild))

    def addChildren(self, children = []):
        for child in children:
            self.children.append(child)

    def addChildrenNode(self, child):
        self.children.append(child)

    def addFirstChild(self, value):
        self.children.insert(0, nodeAST(value))

    def addFirstChildNode(self, child):
        self.children.insert(0, child)

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return str(self.value)

    def getChildren(self):
        return self.children