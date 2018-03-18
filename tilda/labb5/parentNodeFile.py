class ParentNode:
    def __init__(self, string, parent=None):
        self.string = string
        self.parent = parent

    def writechain(self):
        self._writechain(self)
        #print(self.string, end=" ")

    def _writechain(self, child):
        if child.parent != None:
            self._writechain(child.parent)
        print(child.string, end=" ")

