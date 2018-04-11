
class Statistic:
    def __init__(self):
        self.nrComparisons = 0


def mean(data):
    n = 0
    tot = 0
    for i in data:
        n += 1
        tot += i
    return tot/n


def deviation(data, mean):
    x = 0
    for value in data:
        x += (value - mean)**2
    return (x/len(data))**0.5


def median(data):
    quicksort(data)
    return data[len(data)//2]


# ==========================================================================================
# =                        från föreläsning antekningar                                    =
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

# ==========================================================================================