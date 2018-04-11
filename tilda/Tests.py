import numpy as np
import matplotlib.pyplot as plt
from findKthBest import *
from Statistics import *
import random
import math


def k2_test(N, reps):
    dataList = []
    for test in N:
        setList = []
        for k in range(test):
            repList = []
            for i in range(reps):
                s = Statistic()
                data = np.linspace(1, test, test, dtype=int)
                random.shuffle(data)
                findKthBest(k, data, 0, len(data) - 1, s)
                repList.append(s.nrComparisons)
            setList.append(mean(repList))
        dataList.append(setList)
    return dataList


def k_test(N, reps):
    s = Statistic()
    dataList = []
    for k in range(N):
        repList = []
        for i in range(reps):
            s.nrComparisons = 0
            data = np.linspace(1, N, N, dtype=int)
            random.shuffle(data)
            findKthBest(k, data, 0, len(data) - 1, s)
            repList.append(s.nrComparisons)
        dataList.append(repList)
    return dataList


def n_test(N, reps):
    dataList = []
    for test in N:
        setList = []
        # k = random.randint(0,test)
        k = test-1
        # k = test//2
        for i in range(reps):
            s = Statistic()
            data = np.linspace(1, test, test, dtype=int)
            random.shuffle(data)
            findKthBest(k, data, 0, len(data) - 1, s)
            setList.append(s.nrComparisons)
        dataList.append(mean(setList))
    return dataList


def works_test(N, reps):
    s = Statistic()
    tests = 0
    rights = 0
    for test in N:
        for k in range(test):
            for i in range(reps):
                data = np.linspace(0, test-1, test, dtype=int)
                random.shuffle(data)
                r = findKthBest(k, data, 0, len(data) - 1, s)
                tests += 1
                if k == r:
                    rights += 1
                    print("{} = {} rätt: {}/{}".format(r, k, rights, tests))
                else:
                    print("{} != {} fel: {}/{}".format(r, k, rights, tests))
    return [rights/tests * 100, tests, rights]


def mainK2():
    N = 1
    l = [N, 5*N, 10*N, 15*N]
    data = k2_test(l, 1000)

    print(data)
    for series in data:
        plt.scatter(range(len(series)), series, label="N = {}".format(len(series)))

    plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
    plt.xlabel("Sökt element k")
    plt.ylabel("Antal jämförelser")

    plt.show()


def mainK():
    N = 20
    data = k_test(N, 1000)

    meanList = []
    deviationList = []
    medianList = []

    # saveDataKToFile(data)

    # medelvärde
    for set in data:
        meanList.append(mean(set))
        medianList.append(median(set))

    for setIndx in range(N):
        deviationList.append(deviation(data[setIndx], meanList[setIndx]))

    deviationListUpper = np.add(meanList, deviationList)
    deviationListLower = np.subtract(meanList, deviationList)

    print(deviationList)

    kValue = range(N)
    # Plot resultat
    plt.scatter(kValue, meanList, c="b", label="Medelvärde")

    # Plot standardavikelse
    plt.scatter(kValue, deviationListUpper, c="b", marker="_", label="Standardavvikelse")
    plt.scatter(kValue, deviationListLower, c="b", marker="_")

    # Plot standardavikelse
    plt.scatter(kValue, medianList, c="b", marker="x", label="Median")

    # Plot trändlinje
    z = np.polyfit(kValue, meanList, 2)
    p = np.poly1d(z)
    plt.plot(kValue, p(kValue), "r--", label="Trendlinje:\n{}K^2 + {}K + {}"
             .format(z[0].round(2), z[1].round(2), z[2].round(2)))

    # Plot log₂(abs(N/2 - K)) * N
    # plt.plot(kValue, np.log2(abs(N/2 - np.array(kValue)))*N, "k", linewidth=0.5, label="log₂(abs(N/2 - K)) * N")

    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
    plt.title("Grafer 2. k-test N = {}".format(N))
    plt.xlabel("Sökt element k")
    plt.ylabel("Antal jämförelser")
    plt.show()


def mainN():
    N = 100
    l = [N, 5 * N, 10 * N, 15 * N, 20 * N, 25 * N, 30 * N, 40 * N,  60 * N,  100 * N, 150 * N]
    data = n_test(l, 1000)
    x = l
    #print(data)

    # Plot resultat
    plt.scatter(x, data, label="Resultat")

    # Plot N * Pi
    x2 = np.linspace(1, np.array(l).max(), np.array(l).max(), dtype=int)
    plt.plot(x2, x2 * math.pi, "k", linewidth=0.5, label="N * Pi")

    # Plot trendlinje
    z = np.polyfit(x, data, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--", label="Trendlinje:\n{}N + {}".format(z[0].round(2), z[1].round(2)))

    #plt.legend(bbox_to_anchor=(0.05, 0.95), loc=2, borderaxespad=0.)
    plt.title("Grafer 2.1. N-test")
    plt.xlabel("Antal element N")
    plt.ylabel("Antal jämförelser")

    print(z[0].round(2), z[1].round(2))
    #plt.show()


def saveDataKToFile(data):
    text = " repiton -> "
    bar = " --- "
    for rep in range(len(data[0])):
        text += "| {} ".format(rep+1)
        bar += "| --- "
    text += "\n" + bar + "\n"

    for k in range(len(data)):
        text += " k = {} ".format(k)
        for value in data[k]:
            text += "| " + str(value) + " "
        text += "\n"

    writeToFile("test.md", text)


def mainWorks():
    N = 10
    l = [N, 5 * N, 10 * N, 15 * N, 20 * N, 25 * N, 30 * N, 40 * N,  60 * N,  100 * N, 150 * N]
    data = works_test(l, 1000)

    print(data)


def writeToFile(fileName, data):
    file = open(fileName, 'w', encoding="utf-8")
    file.write(data)
    file.close()


#mainWorks()
for i in range(1):
    mainK()
    pass
plt.show()



