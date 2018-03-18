from linkedQFile import LinkedQ

letter = "abcdefghijklmnopqrstuvwxyz"
atoms = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
        'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y',
        'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb','Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce',
        'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir',
        'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm',
        'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Fl', 'Lv']

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
    if queue.peek() == ")" or str(queue.peek()).isdigit():
        raise Syntaxfel("Felaktig gruppstart vid radslutet{}".format(queue.queue()))
    elif queue.peek() == "(":
        # (<mol>) <num>
        queue.dequeue()                             # (
        readMol(queue, True)                        # <mol>
        queue.dequeue()                             # )
        if str(queue.peek()).isdigit():             # <num>
            readNum(queue)
        else:
            raise Syntaxfel("Saknad siffra vid radslutet{}".format(queue.queue()))
    else:
        # <atom> |<atom><num>
        readAtom(queue)
        if str(queue.peek()).isdigit():
            readNum(queue)


def readMol(queue, inParentheses = False):
    """tar in en kö ser om den följer syntaxen
       <mol>   ::= <group> | <group><mol>"""
    readGroup(queue)
    if inParentheses:                    # om mol är inom paranterser
        if queue.peek() == "":
            raise Syntaxfel("Saknad högerparentes vid radslutet{}".format(queue.queue()))
        if queue.peek() != ")":
            readMol(queue, inParentheses)
    else:
        if queue.peek() != "":
            readMol(queue, inParentheses)


def readFormel(queue):
    readMol(queue)


def readAtom(queue):
    """tar in en kö skikar den vidare till readLETTER. efter det kollar den om nästa element
     är en liten bokstav om det är det tas elementet ut"""
    atom = readLETTER(queue)
    if queue.peek() in letter and queue.peek() != "":
        atom += queue.dequeue()
    if not atom in atoms:
        raise Syntaxfel("Okänd atom vid radslutet{}".format(queue.queue()))


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
        return
    raise Syntaxfel("För litet tal vid radslutet{}".format(queue.queue()))


def checkMolekyl(molekyl):
    """tar in en molekyl. skikar molekylen till createQueue som ger tillbacka en kö. kö kontroleras av syntaxen.
    om syntaxen är korekt returnas det att den är rätt anars returnar den felet"""
    queue = createQueue(molekyl)
    try:
        readFormel(queue)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as error:
        return str(error)
    #finally:
        #print(queue.queue())


def createQueue(molekyl):
    """tar in en molekyl som en sträng och läger varje karaktär i en kö
    som retuneras"""
    queue = LinkedQ()
    for char in molekyl:
        queue.enqueue(char)
    return queue


def main():
    molekyl = input()
    while molekyl != "#":
        molekyl.strip("\n")
        result = checkMolekyl(molekyl)
        print(result)
        molekyl = input()


if __name__ == '__main__':
    main()