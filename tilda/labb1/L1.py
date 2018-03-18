import random

class Pokemon:
    def __init__(self, arg):
        self.name = arg[2]
        self.type = arg[10:12]          # 0=type1, 1=type2
        self.stats = arg[3:9]           # 0=max hp, 1=Atk, 2=Def, 3=SpA, 4=SpD, 5=Spe
        self.mass = float(arg[16][0:len(arg[16])-3])
        self.hp = int(arg[3])           # Current HP

    def __str__(self):
        nameString = self.name + " " * (15 - len(self.name))
        statsString = "Stats: HP:%s/%s   Atk:%s   Def:%s   Mass:%s kg" % (self.hp, self.stats[0], self.stats[1],
                                                                          self.stats[2], self.mass)
        statsString = statsString + " " * (55 - len(statsString))
        return nameString + statsString + ("Type:%s %s" % (self.type[0], self.type[1]))

    def __lt__(self, other):
        return self.mass < other.mass

    def takeDamage(self, Dmg):
        """takes a int dmg=damage and
         calculate the damage the Pokemon takes"""
        self.hp -= int(Dmg/(int(self.stats[2])/8))     # self.stats[2] = def

        if self.hp < 0:
            self.hp = 0

    def attack(self, opponent):
        """takes a Pokemon object opponent and
         deals damage to it equal to Atk of this object"""
        if self.hp > 0:
            opponent.takeDamage(int(self.stats[1]))

    def heal(self, hp):
        """takes a int hp and adds it to the objects hp,
         and holding the objects hp under the objects max hp"""
        self.hp += hp

        if self.hp > int(self.stats[0]):
            self.hp = self.stats[0]


class Gym:
    def __init__(self, name, pokemons):
        self.name = name
        self.gymList = pokemons

    def __str__(self):
        string = "="*30 + "  %s Gym  " % self.name + "="*30
        for pokemon in self.gymList:
            string += "\n%s" % pokemon
        return string

    def searchPokemon(self, search):
        matchList = []

        for gymPokemon in self.gymList:
            if gymPokemon.name.lower() == search.lower():       # or gymPokemon.type[0].lower() == search.lower():
                matchList.append(gymPokemon)

        return matchList


def createPokemon(arg):
    """creates a Pokemon object with a list arg as its arguments"""
    return Pokemon(arg)


def readFile(file):
    """takes a string file and open the file whit file as name,
     read the content and returns it as a string"""
    file = open(file, 'r', encoding="utf-8")
    text = file.read()
    file.close()

    return text


def createPokemonList(file):
    """creates Pokemon objects for all the pokemons in a file"""
    pokemonList = []
    text = readFile(file)
    pokemons = text.split("\n")

    for pokemon in pokemons[1:]:
        arg = pokemon.split(",")
        pokemonList.append(createPokemon(arg))

    return pokemonList


def createGym(gymName, plist):
    gymList = []
    for i in range(5):
        pokemonIndx = random.randint(0, len(plist))
        gymList.append(plist[pokemonIndx])

    return Gym(gymName, gymList)


def yourePokemon(plist):
    pokemonIndx = random.randint(0, len(plist))
    return plist[pokemonIndx]


def main():
    pokemonList = createPokemonList("Pokedex.csv")
    youreP = yourePokemon(pokemonList)
    gym = createGym("bla", pokemonList)
    while(1):
        print(gym, '\n')
        print("you're pokemon:")
        print(youreP, '\n')

        inp = input("a = Atk, h = heal: ")
        if inp == "a":
            which = input("which: ")
            youreP.attack(gym.searchPokemon(which)[0])
            gym.searchPokemon(which)[0].attack(youreP)
        elif inp == "h":
            hp = int(input("hp: "))
            youreP.heal(hp)


if __name__ == '__main__':
    main()
    """pokemonList = createPokemonList("Pokedex.csv")
    blaGym = Gym("bla", pokemonList[10:20])
    matchList = blaGym.searchPokemon("Weedle")
    for p in matchList:
        print(p)
    print(blaGym)
    print(pokemonList[0], "==", pokemonList[1])
    pokemonList[0].takeDamage(10)
    pokemonList[0].attack(pokemonList[1])
    print(pokemonList[0],"==", pokemonList[1])
    pokemonList[0].heal(80)
    print(pokemonList[0], "==", pokemonList[1])

    print("\n==============")
    if pokemonList[0] < pokemonList[1]:   # 6.9 kG, 13.0 kG
        print("y")

    print("\n==============")
    emilioGym = Gym("Emilio", pokemonList[10:20])
    print(emilioGym)

    print("\n==============")
    for pokemon in pokemonList:
        if pokemon < pokemonList[11]:
            print(pokemon)"""
