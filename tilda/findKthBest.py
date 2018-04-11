import random


def findKthBest(k, data, low, high, statistik):
    pivotindex = random.randint(low, high)
    # flytta pivot till kanten
    data[pivotindex], data[high] = data[high], data[pivotindex]

    # damerna först med avseende på pivotdata
    pivotmid = partitionera(data, low-1, high, data[high], statistik)

    # flytta tillbaka pivot
    data[pivotmid], data[high] = data[high], data[pivotmid]

    statistik.nrComparisons += 1
    if pivotmid == k:
        return data[pivotmid]
    elif k < pivotmid:
        return findKthBest(k, data, low, pivotmid - 1, statistik)
    else:
        return findKthBest(k, data, pivotmid + 1, high, statistik)


def partitionera(data, v, h, pivot, statistik):
    while True:
        v = v + 1
        while data[v] < pivot:              # <
            statistik.nrComparisons += 1
            v = v + 1
        h = h - 1    # hoppa över pivot
        while h != 0 and data[h] > pivot:   # >
            statistik.nrComparisons += 1
            h = h - 1
        data[v], data[h] = data[h], data[v]
        if v >= h:
            break
    data[v], data[h] = data[h], data[v]
    return v


class stat:
    def __init__(self):
        self.nrComparisons = 0

if __name__ == '__main__':
    L = [1, 6, 4, 2, 8, 9, 7]
    s = stat()
    print(findKthBest(0, L, 0, len(L) - 1, s))
    print(s.nrComparisons)
    print(L)