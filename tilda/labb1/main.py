import random

class Pokemon:
    def __init__(self, arg):        # 0=name 1=types  2=stats 3=mass
        self.name = arg[0]
        self.type = arg[1]          # 0=type1, 1=type2
        self.stats = []
        for stat in arg[2]:         # 0=hp, 1=Atk, 2=Def
            self.stats.append(int(stat))
        self.mass = arg[3]
        self.hp = self.stats[0]       # Current HP

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
        """returns a pokemon with the name or type ett equal to search"""
        matchList = []

        for gymPokemon in self.gymList:
            if gymPokemon.name.lower() == search.lower() or gymPokemon.type[0].lower() == search.lower():
                matchList.append(gymPokemon)

        return matchList


def testPokemon():
    """test the Pokemon class"""
    pokemon1 = Pokemon(["bob", ["Grass", ""], [100, 120, 120], 800.9])
    pokemon2 = Pokemon(["kurt", ["Grass", ""], [90, 150, 110], 1000.9])
    if pokemon1 > pokemon2:
        print(True, '\n')
    else:
        print(False, '\n')
    print(pokemon1, pokemon2)
    pokemon1.attack(pokemon2)
    print(pokemon1, pokemon2)
    pokemon2.heal(10)
    print(pokemon1, pokemon2)


def createPokemon(arg):
    """creates a Pokemon object with a list arg as its arguments"""
    pokemonArg = []
    pokemonArg.append(arg[2]) # name
    pokemonArg.append(arg[10:12])  # 0=type1, 1=type2
    pokemonArg.append(arg[3:7])  # 0=max hp, 1=Atk, 2=Def, 3=SpA, 4=SpD, 5=Spe
    pokemonArg.append(float(arg[16].strip(" KGkg")))
    return Pokemon(pokemonArg)


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
    """creates a gym with 5 random pokemon from plist"""
    gymList = []
    for i in range(5):
        pokemonIndx = random.randint(0, len(plist))
        gymList.append(plist[pokemonIndx])

    return Gym(gymName, gymList)


def yourePokemon(plist):
    """gives the user a random pokemon"""
    pokemonIndx = random.randint(0, len(plist))
    return plist[pokemonIndx]


def main():
    """the main loop"""
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
    #testPokemon()
    main()