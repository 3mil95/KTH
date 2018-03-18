import numpy as np
import scipy.fftpack as fft
import scipy.signal
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile


T1 = "dtmf_1.wav"
T2 = "dtmf_2.wav"
Ta = "dtmf_all.wav"


def spektrum(X, fs):
    N = len(X)
    Y = fft.fft(X)
    Y = np.square(np.abs(Y))
    Y /= X.max() * N

    w = np.linspace(0,fs,N)

    B = int(N/2)
    b = Y[0:B]
    a = w[0:B]

    plt.plot(a, b)
    plt.show()


def avkodning(X, fs):
    N = len(X)
    Y = fft.fft(X)
    Y = np.square(np.abs(Y))
    Y /= X.max()*N

    #Hz
    lowHz = np.array([697, 770, 852, 941])
    highHz = np.array([1209, 1336, 1477, 1633])
    #k
    klow = (lowHz * N / fs).astype(int)
    khigh = (highHz * N / fs).astype(int)
    #E
    Elow = np.array([Y[klow[0]], Y[klow[1]], Y[klow[2]], Y[klow[3]]])
    Ehigh = np.array([Y[khigh[0]], Y[khigh[1]], Y[khigh[2]], Y[khigh[3]]])

    T = (1/2.3 * Y.max())**2

    S = ''
    if (Elow[0] * Ehigh[0]) > T:
        S = '1'
    elif (Elow[0] * Ehigh[1]) > T:
        S = '2'
    elif (Elow[0] * Ehigh[2]) > T:
        S = '3'
    elif (Elow[0] * Ehigh[3]) > T:
        S = 'A'
    elif (Elow[1] * Ehigh[0]) > T:
        S = '4'
    elif (Elow[1] * Ehigh[1]) > T:
        S = '5'
    elif (Elow[1] * Ehigh[2]) > T:
        S = '6'
    elif (Elow[1] * Ehigh[3]) > T:
        S = 'B'
    elif (Elow[2] * Ehigh[0]) > T:
        S = '7'
    elif (Elow[2] * Ehigh[1]) > T:
        S = '8'
    elif (Elow[2] * Ehigh[2]) > T:
        S = '9'
    elif (Elow[2] * Ehigh[3]) > T:
        S = 'C'
    elif (Elow[3] * Ehigh[0]) > T:
        S = '*'
    elif (Elow[3] * Ehigh[1]) > T:
        S = '0'
    elif (Elow[3] * Ehigh[2]) > T:
        S = '#'
    elif (Elow[3] * Ehigh[3]) > T:
        S = 'D'
    return S


def sekvens(X, fs, t_ms=20):
    l = int(fs * t_ms / 1000)

    sek = []
    for i in range(0,len(X),l):
        if len(X[i:i+l]) >= 100:
            Y = np.append(X[i:i+l], np.zeros(280))
            sek.append(avkodning(Y, fs))

    sek.append("<")
    ft = ""
    i = 0
    while sek[i] != "<":
        if sek[i] != ft:
            ft = sek[i]
            if sek[i] == '':
                sek.pop(i)
            else:
                i += 1
        else:
            sek.pop(i)
    sek.pop(len(sek)-1)

    return sek


if __name__ == '__main__':
    fs, X = scipy.io.wavfile.read(Ta)
    fs, X2 = scipy.io.wavfile.read(T2)
    # Uppgift 4
    #sek = sekvens(X, fs)
    #print(sek)
    # Uppgift 3
    #S = avkodning(X, fs)
    #print(S)
    #S = avkodning(X2, fs)
    #print(S)
    #Uppgift 2
    spektrum(X2, fs)

