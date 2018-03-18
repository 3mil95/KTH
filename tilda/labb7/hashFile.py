hashalf = "abcdefghijklmnopqrstuvwxyz"

class HashNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def __str__(self):
        return "Key: %s  Data: %s" % (self.key, self.value)


class Hashtabell:
    def __init__(self, size):
        self.size = findPrime(size * 2)
        self.collisions = 0
        self.list = []
        for i in range(self.size):
            self.list.append(HashNode())

    def __getitem__(self, nyckel):
        return self.search(nyckel)

    def __contains__(self, nyckel):
        try:
            self.search(nyckel)
            return True
        except KeyError:
            return False

    def store(self, key, data):
        """sorterar in data i en hashtabell med nyckeln key"""
        num = hashfunction(key, self.size)
        while True:
            if self.list[num].key == None:
                self.list[num].key = key
                self.list[num].value = data
                break
            print("krock " + key)
            self.collisions += 1
            num += 1
            if num >= self.size:
                num = 0

    def search(self, key):
        """hitar data som tillhör nycken key"""
        num = hashfunction(key, self.size)
        while True:
            if self.list[num].key == key:
                return self.list[num].value
            if self.list[num].key == None:
                raise KeyError
            num += 1
            if num >= self.size:
                num = 0


def findPrime(num):
    """hitar ett primtal som är störe en num"""
    found = False
    while not found:
        found = True
        for i in range(2, num // 2):
            if num % i == 0:
                found = False
                num += 1
                break
    return num


def hashfunction(key, size):
    """tar en key och size och räknar ut indexet i hashtabell för nycken key"""
    hashIndex = 0
    num = 1
    for charakter in key:
        hashIndex += hashalf.find(charakter.lower()) * 4 * num
        num *= 100
        #hashs += ord(charakter) ^ num
        #hashs += ord(charakter) * num
        #num *= 120
        #num += 1
    return hashIndex % size


def test():
    h = Hashtabell(4)
    h.store("hej", "hi")
    h.store("apa", "blö")
    h.store("1", "123")
    h.store("hkapa", "mo")
    for i in h.list:
        print(i)

    if "apa" in h:
        print(h["apa"])
    if "app" in h:
        print("app")
    else:
        print("ej app")

    print("Krockar: ", h.collisions)


if __name__ == '__main__':
    test()
