from linkedQFile import LinkedQ
from molgrafik import *

letter = "abcdefghijklmnopqrstuvwxyz"
atomDict = {}

def createDict():
    """leger in atomer och dens vikt från atom.txt"""
    file = open("atom.txt", "r")
    text = file.read()
    for a in text.split("\n"):
        a = a.split(";")
        atomDict[a[0]] = a[1].strip()


class Syntaxfel(Exception):
    """ <formel>::= <mol> \n
        <mol>   ::= <group> | <group><mol>
        <group> ::= <atom> |<atom><num> | (<mol>) <num>
        <atom>  ::= <LETTER> | <LETTER><letter>
        <LETTER>::= A | B | C | ... | Z
        <letter>::= a | b | c | ... | z
        <num>   ::= 2 | 3 | 4 | ..."""
    pass


def readGroup(queue):
    """tar in en queue ser om den följer syntaxen
       <group> ::= <atom> |<atom><num> | (<mol>) <num>"""
    rutan = Ruta()
    if queue.peek() == ")" or str(queue.peek()).isdigit():
        raise Syntaxfel("Felaktig gruppstart vid radslutet{}".format(queue.queue()))
    elif queue.peek() == "(":
        # (<mol>) <num>
        queue.dequeue()                             # (
        rutan.down = readMol(queue, True)           # <mol>
        queue.dequeue()                             # )
        if str(queue.peek()).isdigit():             # <num>
            rutan.num = readNum(queue)
        else:
            raise Syntaxfel("Saknad siffra vid radslutet{}".format(queue.queue()))
    else:
        # <atom> | <atom><num>
        rutan.atom = readAtom(queue)
        if str(queue.peek()).isdigit():
            rutan.num = readNum(queue)
    return rutan


def readMol(queue, inParentheses = False):
    """tar in en kö ser om den följer syntaxen
       <mol>   ::= <group> | <group><mol>"""
    mol = readGroup(queue)
    if inParentheses:                       # om mol är inom paranterser
        if queue.peek() == "":
            raise Syntaxfel("Saknad högerparentes vid radslutet{}".format(queue.queue()))
        if queue.peek() != ")":
            mol.next = readMol(queue, inParentheses)
    else:
        if queue.peek() != "":
            mol.next = readMol(queue, inParentheses)
    return mol


def readFormel(queue):
    mol = readMol(queue)
    return mol


def readAtom(queue):
    """tar in en kö skikar den vidare till readLETTER. efter det kollar den om nästa element
     är en liten bokstav om det är det tas elementet ut"""
    atom = readLETTER(queue)
    if queue.peek() in letter and queue.peek() != "":
        atom += queue.dequeue()
    if not atom in atomDict:
        raise Syntaxfel("Okänd atom vid radslutet{}".format(queue.queue()))
    return atom

def readLETTER(queue):
    """tar in en kö. tar ut det första elementen och kollar om det är en stor bokstav
    om det är en stor bokstav reternar funktionen anars raiseas ett Syntaxfel Saknad stor bokstav"""
    chrarecter = str(queue.dequeue())
    if chrarecter in letter.upper():
        return chrarecter
    left = " " + chrarecter + (queue.queue()).strip(" ")
    raise Syntaxfel("Saknad stor bokstav vid radslutet{}".format(left))


def readNum(queue):
    """tar in en kö. tar ut det första elementet som är en int. så länge som nesta element är en int legs de ihop.
     elementet kontroleras att det är störe än ett då returnar funktione anars returnas syntax fel"""
    chrarecter = queue.dequeue()
    if int(chrarecter) > 0:
        while str(queue.peek()).isdigit():
            chrarecter += queue.dequeue()
    if int(chrarecter) > 1:
        return int(chrarecter)
    raise Syntaxfel("För litet tal vid radslutet{}".format(queue.queue()))


def checkMolekyl(molekyl):
    """tar in en molekyl. skikar molekylen till createQueue som ger tillbacka en kö. kö kontroleras av syntaxen.
    om syntaxen är korekt returnas det att den är rätt anars returnar den felet"""
    queue = createQueue(molekyl)
    try:
        mol = readFormel(queue)
        return "Formeln är syntaktiskt korrekt", mol
    except Syntaxfel as error:
        return str(error), None


def createQueue(molekyl):
    """tar in en molekyl som en sträng och läger varje karaktär i en kö
    som retuneras"""
    queue = LinkedQ()
    for char in molekyl:
        queue.enqueue(char)
    return queue


def weight(mol):
    if mol.down == None:
        if mol.next != None:
            return float(atomDict[mol.atom]) * int(mol.num) + weight(mol.next)
        return float(atomDict[mol.atom]) * int(mol.num)
    else:
        if mol.next != None:
            return weight(mol.down) * int(mol.num) + weight(mol.next)
        return weight(mol.down) * int(mol.num)


def main():
    molekyl = input("Molekyl: ")
    while molekyl != "#":
        molekyl.strip("\n")
        result, mol = checkMolekyl(molekyl)
        print(result)
        if result == "Formeln är syntaktiskt korrekt":
            print("Vikt: {}".format(weight(mol)))
            print("Ritar")
            mg = Molgrafik()
            mg.show(mol)
        molekyl = input("Molekyl: ")


if __name__ == '__main__':
    createDict()
    main()
