from bintreeFile import Bintree


def createSwedishTree():
    """creates the tree and prints duplicates"""
    with open("word3.txt", "r", encoding="utf-8") as swedishFile:
        for row in swedishFile:
            word = row.strip()
            if word in swedish:
                print(word, end=" ")
            else:
                swedish.put(word)
    swedishFile.close()
    print("\n")


def createEnglishTree():
    """creates the english tree and if a word exists in
    the swedish tree the word is printed out"""
    englishFile = open("engelska.txt", "r", encoding="utf-8")
    englishWorde = englishFile.read()
    englishWorde = englishWorde.split(" ")
    for word in englishWorde:
        word = word.strip("'!, ")
        if not word in english:
            english.put(word)
            if word in swedish:
                print(word, end=" ")
    englishFile.close()


if __name__ == '__main__':
    english = Bintree()
    swedish = Bintree()
    createSwedishTree()
    createEnglishTree()

