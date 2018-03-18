from bintreeFile import Bintree
from linkedQFile import LinkedQ
from parentNodeFile import ParentNode

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


def main():
    # user input
    startWord = ParentNode(userInput("startord: "))
    endWord = userInput("slutord: ")
    # search
    old.put(startWord.string)
    queue.enqueue(startWord)
    found, word = search(endWord)
    # print
    if found:
        print("Det finns en väg till", endWord)
        word.writechain()
    else:
        print("Det finns inte en väg till", endWord)


def search(endWord):
    """gos through the queue and search after the end word and
    if it found the function returns true and the wordNode otherwise it returns false and None"""
    found = False
    while not queue.isEmpty() and not found:
        wordNode = queue.dequeue()
        found, wordNode = makeChildren(wordNode, endWord)
    return found, wordNode


def makeChildren(startword, endWord):
    """takes a word and looks through all the possible words that can be created by changing a letter,
        if the new word exist in the swedish tree and not in the english tree the word is added to the queue
        if the newWord is the end word the function returns tro and the word node else false and none"""
    for letter in range(len(startword.string)):
        for character in alphabet:
            newWord = startword.string[0:letter] + character + startword.string[letter+1:]
            if newWord in swedish and not newWord in old:
                newWordNode = ParentNode(newWord, startword)
                if newWord == endWord:
                    return True, newWordNode
                old.put(newWordNode.string)
                queue.enqueue(newWordNode)
    return False, None

if __name__ == '__main__':
    queue = LinkedQ()
    old = Bintree()
    swedish = Bintree()
    createTree()
    main()

