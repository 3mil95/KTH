from bintreeFile import Bintree
from linkedQFile import LinkedQ

alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'

def createTree():
    """creates the swedish tree"""
    with open("word3.txt", "r", encoding="utf-8") as swedishfile:
        for row in swedishfile:
            word = row.strip()
            swedish.put(word)
    swedishfile.close()


def userInput(inputString):
    """returns a user input"""
    outputString = input(inputString)
    return outputString


def search(endWord):
    """gos through the queue and search after the end word and
    if it found the function returns true otherwise it returns false"""
    found = False
    while not queue.isEmpty() and not found:
        word = queue.dequeue()
        found = makeChildren(word, endWord)
    return found


def makeChildren(startword, endWord):
    """takes a word and looks through all the possible words that can be created by changing a letter,
    if the new word exist in the swedish tree and not in the old tree the word is added to the queue.
    if the new word is the endWord the function returns true"""
    for letter in range(len(startword)):
        for character in alphabet:
            newWord = startword[0:letter] + character + startword[letter+1:]
            if endWord == newWord:
                return True
            if newWord in swedish and not newWord in old:
                old.put(newWord)
                queue.enqueue(newWord)
                #print(newWord)
    return False


def main():
    createTree()
    # user input
    startWord = userInput("startord: ")
    endWord = userInput("slutord: ")
    # search
    old.put(startWord)
    queue.enqueue(startWord)
    found = search(endWord)
    # print
    if found:
        print("Det finns en väg till", endWord)
    else:
        print("Det finns inte en väg till", endWord)


if __name__ == '__main__':
    queue = LinkedQ()
    old = Bintree()
    swedish = Bintree()
    main()

