import timeit
from trackFile import Track, Track2
from math import log2

valueFigures = 5
repeats = 1000

# ==========================================================================================
# =                        från föreläsning antekningar 3 och 7                            =
# ==========================================================================================

def quicksort(data):
    sista = len(data) - 1
    qsort(data, 0, sista)


def qsort(data, low, high):
    pivotindex = (low + high) // 2
    # flytta pivot till kanten
    data[pivotindex], data[high] = data[high], data[pivotindex]

    # damerna först med avseende på pivotdata
    pivotmid = partitionera(data, low - 1, high, data[high])

    # flytta tillbaka pivot
    data[pivotmid], data[high] = data[high], data[pivotmid]

    if pivotmid - low > 1:
        qsort(data, low, pivotmid - 1)
    if high - pivotmid > 1:
        qsort(data, pivotmid + 1, high)


def partitionera(data, v, h, pivot):
    while True:
        v = v + 1
        while data[v] < pivot:
            v = v + 1
        h = h - 1
        while h != 0 and data[h] > pivot:
            h = h - 1
        data[v], data[h] = data[h], data[v]
        if v >= h:
            break
    data[v], data[h] = data[h], data[v]
    return v


def binary_search(the_list, key):
   low = 0
   high = len(the_list)-1
   found = False

   while low <= high and not found:
      middle = (low + high)//2
      if the_list[middle] == key:
         found = True
      else:
         if key < the_list[middle]:
            high = middle - 1
         else:
            low = middle + 1
   return found


def mergesort(data):
    if len(data) > 1:
        mitten = len(data)//2
        vensterHalva = data[:mitten]
        hogerHalva = data[mitten:]

        mergesort(vensterHalva)
        mergesort(hogerHalva)

        i, j, k = 0, 0, 0

        while i < len(vensterHalva) and j < len(hogerHalva):
            if vensterHalva[i] < hogerHalva[j]:
                data[k] = vensterHalva[i]
                i = i + 1
            else:
                data[k] = hogerHalva[j]
                j = j + 1
            k = k + 1

        while i < len(vensterHalva):
            data[k] = vensterHalva[i]
            i = i + 1
            k = k + 1

        while j < len(hogerHalva):
            data[k] = hogerHalva[j]
            j = j + 1
            k = k + 1

# ==========================================================================================


def readfile(filename, n, split, part):
    """öppnar filen filename och delar upp den rad för rad och splitar med strängen split
    och returnar en list och en dictionary beronde på part"""
    songList = []
    songDict = {}
    with open(filename, 'r', encoding="utf-8") as file:
        for song in file:
            song = song.strip().split(split)
            if part == 1:
                songList.append(Track(song[0], song[1], song[2], song[3]))
                songDict[song[2]] = Track(song[0], song[1], song[2], song[3])
            else:
                songList.append(Track2(song[0], song[1], song[2], song[3], song[4]))
            n -= 1
            if n == 0:
                break
    file.close()
    return songList, songDict


def writeToFile(fileName, data):
    """skriver data till en file med namn fileName"""
    file = open(fileName, 'w', encoding="utf-8")
    file.write(data)
    file.close()


def linSerch(lista, test):
    """söker linjärt efter ett element test"""
    found = False
    for song in lista:
        if song.artistName == test:
            found = song
    return found


def dictSerch(dict, test):
    """söker ett elemnt test med hjälp av dictionary"""
    return dict[test]


def sortedFoundLongest(list, index):
    """hitar den index:e längsta i en lista med hjälp av quicksort"""
    quicksort(list)
    return list[-index]


def foundLongest(list, index, compare=Track2(None, None, None, 0, None)):
    """hitar den index:e längsta i en lista med flera linjär sökningar"""
    fuondDict = {}
    maxLenth = compare
    for n in range(index):
        maxLenth = compare
        for i in list:
            if i > maxLenth and not i in fuondDict:
                maxLenth = i
        fuondDict[maxLenth] = True

    return maxLenth


def mainOne(n):
    """ del 1 test"""
    filename = "C:/Users/Emil Clemedson/PycharmProjects/Emil/KTH/Tilda/unique_tracks.txt"

    lista, dictionary = readfile(filename, n, "<SEP>", 1)

    sista = lista[n-1]
    testartist = sista.artistName

    # tidtagning
    linjtid = timeit.timeit(stmt=lambda: linSerch(lista, testartist), number=repeats)
    sortTime = timeit.timeit(stmt=lambda: quicksort(lista), number=repeats)
    binarySearchTime = timeit.timeit(stmt=lambda: binary_search(lista, sista), number=repeats)
    dicttid = timeit.timeit(stmt=lambda: dictSerch(dictionary, testartist), number=repeats)

    return "\n {} | {} | {} | {} | {}".format(n, round(linjtid, valueFigures), round(sortTime, valueFigures),
                                              round(binarySearchTime, valueFigures), round(dicttid, valueFigures))

def mainTwo(n, k):
    """del 2 test"""
    filename = "C:/Users/Emil Clemedson/PycharmProjects/Emil/KTH/Tilda/sang-artist-data.txt"

    lista, dict = readfile(filename, n, "\t", 2)

    # unsorted
    head = "N=" + str(n) + ' '
    headdiv = " --- "
    data = 'Osorterad '
    for i in range(1, k+1):
        # head
        if i//10 != 1 and i % 10 == 1 or i % 10 == 2:
            head += "| {}:a längsta ".format(i)
        else:
            head += "| {}:e längsta ".format(i)
        # headdiv
        headdiv += "| ---"
        # data
        data = data + ' | ' + str(round(timeit.timeit(stmt=lambda: foundLongest(lista, i), number=repeats),
                                        valueFigures))
    head += '\n'
    headdiv += '\n'

    data = head + headdiv + data + '\n'

    # sorted
    data += "sorterad"
    for i in range(1, k + 1):
        data += '| ' + str(round(timeit.timeit(stmt=lambda: sortedFoundLongest(lista, i), number=repeats),
                                 valueFigures))

    return data


def theoryPartTow(nlist):
    """returnar de teoretiskt bäräkningar"""
    data = """ 
    
Med sortering behövs N * log2(N) och utan N * index från max (index=1 är max)
      
N | vilket index som det blir mer efektift med sortering
--- | ---
"""
    for n in nlist:
        for i in range(1, n):
            sortSertc = n * log2(n)
            if sortSertc < n * i:
                data += " {} | {} \n".format(n, i)
                break

    return data


def main(nListPart1, nListPart2, indexs=10):
    """main"""
    data =""
    # del 1
    if len(nListPart1) > 0:
        data = """## Del 1
        
        N | Linjärsökningen O(N) | Quicksort O(N*log(N)) | Binarysökningen O(N*log(N)) | Dictsökningen O(1)
        --- | --- |  --- | --- | ---"""
        for n in nListPart1:
            data += mainOne(n)
        print("Del 1 Done!")

    # del 2
    if len(nListPart2) > 0:
        data += """    

## Del 2
        """
        data += theoryPartTow(nListPart2) + '\n'
        for n in nListPart2:
            data += mainTwo(n, indexs) + '\n' * 2
        print("Del 2 Done!")

    writeToFile('Analys4.md', data)
    print("Done!")


if __name__ == '__main__':
    main([10, 15], [10])