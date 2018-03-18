class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None


class Bintree:
    def __init__(self):
        self.root = None

    def put(self, newvalue):
        """Sorterar in newvalue i trädet"""
        if self.root == None:
            self.root = Node(newvalue)
        else:
            self.root = putta(self.root, newvalue)

    def __contains__(self, value):
        """True om value finns i trädet, False annars"""
        return finns(self.root, value)

    def write(self):
        """"Skriver ut trädet i inorder"""
        # print(skriv(self.root))
        skriv(self.root)
        print("\n")


def putta(node, newvalue):
    """en rekursiva hjälpfunktioner till put"""
    if newvalue < node.value:
        if node.left == None:
            node.left = Node(newvalue)
        else:
            putta(node.left, newvalue)
    elif newvalue > node.value:
        if node.right == None:
            node.right = Node(newvalue)
        else:
            putta(node.right, newvalue)
    return node


def skriv(node):
    """en rekursiva hjälpfunktioner till write"""
    if node != None:
        skriv(node.left)
        print(node.value, end=' ')
        skriv(node.right)


def finns(node, value):
    """en rekursiva hjälpfunktioner till __contains__"""
    if node == None:
        return False
    elif value == node.value:
        return True
    elif value < node.value:
        return finns(node.left, value)
    else:
        return finns(node.right, value)


def test():
    """testar Bintree klassen"""
    tree = Bintree()
    putList = [8, 2, 3, 6, 4]
    for x in putList:
        tree.put(x)

    for n in range(9):
        if n in tree:
            print(n, 'finns')
        else:
            print(n, 'finns inte')

    tree.write()


if __name__ == '__main__':
    test()

