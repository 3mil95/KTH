import array
from arrayQFile import ArrayQ
from linkedQFile import LinkedQ


def theWizardProgramMain():
    """simulates a magic trick"""
    cards = theWizardProgramInput()
    theWizardProgramNewCardPos(cards)


def theWizardProgramInput():
    """gets a input from user and
    converts the input to a list of ints and returns it"""
    while(True):
        cardText = input("Vilken ordning ligger korten i?: ")
        try:
            cardList = cardText.split(',')
            cardList = [int(card) for card in cardList]
            break
        except:
            print("fel")
    return cardList


def theWizardProgramNewCardPos(cards):
    """takes a list of cards and
     prints the new order after the trick"""
    # cardQueue = LinkedQ()             # Using LinkedQ
    cardQueue = ArrayQ()                # Using ArrayQ
    # adds the cards to the queue
    for card in cards:
        cardQueue.enqueue(card)

    # create the output string
    string = "De kommer ut i denna ordning:"    # 7, 1, 12, 2, 8, 3, 11, 4, 9, 5, 13, 6, 10  =>
                                                # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
    while not cardQueue.isEmpty():
        cardQueue.enqueue(cardQueue.dequeue())
        string = string + ' ' + str(cardQueue.dequeue())

    print(string)


if __name__ == '__main__':
    theWizardProgramMain()

    # Array test
    a = array.array('i', [0, 1])
    a.append(5)
    a.append(2)
    a.insert(0, 4)