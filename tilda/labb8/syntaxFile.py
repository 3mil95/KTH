from linkedQFile import LinkedQ

letter = "abcdefghijklmnopqrstuvwxyz"

class Syntaxfel(Exception):
    """<molekyl> ::= <atom> | <atom><num> (| <atom><molekyl> | <atom><num><molekyl>)
        <atom>  ::= <LETTER> | <LETTER><letter>
        <LETTER>::= A | B | C | ... | Z
        <letter>::= a | b | c | ... | z
        <num>   ::= 2 | 3 | 4 | ... """
    pass


def readMolekyl(queue):
    """tar in en kö, om kön är tom returanr funktionen anars skikas kö till readAtom
    där efter kolar fuktionen om nästa i kö är en int om det är en int skikas kön till readNum"""
    #if queue.peek() == "":
    #    return
    readAtom(queue)
    if str(queue.peek()).isdigit():
        readNum(queue)
    #readMolekyl(queue)


def readAtom(queue):
    """tar in en kö skikar den vidare till readLETTER. efter det kollar den om nästa element
     är en liten bokstav om det är det tas elementet ut"""
    readLETTER(queue)
    if queue.peek() in letter:
        #readLetter(queue)
        chrarecter = queue.dequeue()


def readLETTER(queue):
    """tar in en kö. tar ut det första elementen och kollar om det är en stor bokstav
    om det är en stor bokstav reternar funktionen anars raiseas ett Syntaxfel Saknad stor bokstav"""
    chrarecter = str(queue.dequeue())
    if chrarecter in letter.upper():
        return
    raise Syntaxfel("Saknad stor bokstav")


def readNum(queue):
    """tar in en kö. tar ut det första elementet som är en int. så länge som nesta element är en int legs de ihop.
     elementet kontroleras att det är störe än ett då returnar funktione anars returnas syntax fel"""
    chrarecter = queue.dequeue()
    while str(queue.peek()).isdigit():
        chrarecter += queue.dequeue()
    if int(chrarecter) > 1:
        return
    raise Syntaxfel("För litet tal vid radslutet")


def checkMolekyl(molekyl):
    """tar in en molekyl. skikar molekylen till createQueue som ger tillbacka en kö. kö kontroleras av syntaxen.
    om syntaxen är korekt returnas det att den är rätt anars returnar den felet"""
    queue = createQueue(molekyl)
    try:
        readMolekyl(queue)
        return "Formeln är syntaktiskt korrekt!"
    except Syntaxfel as error:
        return str(error)


def createQueue(molekyl):
    """tar in en molekyl som en sträng och läger varje karaktär i en kö
    som retuneras"""
    queue = LinkedQ()
    for char in molekyl:
        queue.enqueue(char)
    return queue


def test():
    result = checkMolekyl("Aa4B7Cc33")
    print(result)

def main():
    while True:
        molekyl = input("Skriv en molekyl: ")
        result = checkMolekyl(molekyl)
        print(result)


if __name__ == '__main__':
    #test()
    main()