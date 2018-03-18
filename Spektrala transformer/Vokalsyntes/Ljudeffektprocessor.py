import numpy as np
import simpleaudio as sa
import scipy
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import time
import matplotlib.pyplot as plt
import scipy.fftpack as fft


def chorusFlanger(X, D, f, md, a, b, fs):
    Y = np.zeros(len(X) + int(D+md))
    D = fs * D / 1000
    f = f / fs

    for i in range(len(X)):
        t = int(D * (1 + md * np.sin(2 * np.pi * f * i)))
        Y[i] = a * X[i] + b * X[i - t]

    return Y[0:len(X)]


def reverbEko(X, D, a, b, fs):
    D = int(fs * D /1000)
    A = [a]
    B = np.zeros(D+1)
    B[0] = 1
    B[D] = b
    Y = scipy.signal.lfilter(B, A, X)

    return Y

def pongDelay(X, D, a, b, fs):
    if len(X[0]) == 2:
        Dn = int(fs * D / 1000)
        X[:, 0] = reverbEko(X[:, 0], D, a, b, fs)
        X[:, 1] = reverbEko(X[:, 1], D, a, b, fs)
        Y = np.append(np.zeros(Dn), X[:, 1])
        X[:, 1] = Y[0:len(X[:, 1])]
    else:
        X = reverbEko(X, D, a, b, fs)

    return X


def softClipping(X, G, V):
    Xm = X.max()
    X = X / 32767 * G
    Y = (X - X**3/3)
    Y = np.where(Y <= 1, Y, 2/3)
    Y = np.where(Y >= -1, Y, -2/3)
    Y *= (Xm / Y.max())
    print(Y, '\n')

    return Y


def hardClipping(X, G, V):
    Xm = X.max()
    X = X / 32767 * G
    Y = X
    Y = np.where(Y <= 1, Y, 1)
    Y = np.where(Y >= -1, Y, -1)
    Y *= Xm

    return Y


def whawha(X, S, Fm, dF, BW, fs):
    T = np.array(range(len(X)))
    S = 2 * np.pi * S / fs
    F = Fm - dF * np.sin(S*T)
    if len(X[0]) == 2:
        X[:, 0] = formantfilter(X[:, 0], F, BW)
        X[:, 1] = formantfilter(X[:, 1], F, BW)
    else:
        X = formantfilter(X, F, BW)

    return X


def formantfilter(X, F, BW):
    R = 1 - BW / 2

    X = np.append([0,0], X)
    Y = np.zeros(len(X))
    for i in range(2, len(X)):
        theta = 2 * np.pi * F[i-2]
        Y[i] = (1 - R ** 2) * np.sin(theta)*X[i] +2 * R * np.cos(theta)*Y[i-1] - R ** 2 * Y[i-2]
    return Y[2:]


def bitkross(X, bitar):
    m = np.array([X.max(), X.min()])
    X = X/abs(m.max())
    X = X*((2**bitar/2)-0.9)
    X = np.floor(X)
    X = X/((2**bitar/2)-0.9)
    X = X*abs(m.max())
    return X


def tremalo1(X, S, dep, typ, fs):
    dep /= 2
    t = np.array(range(len(X)))
    S = 2 * np.pi * S / fs
    if typ == 1:
        t = (1-dep) - dep * np.sin(S * t)
    else:
        w = np.sin(S * t)
        w = np.where(w<0, -1, 1)
        t = (1 - dep) - dep * w
    X = X * t

    return X


def compresor(X):
    X = np.where(X < 0.1 , X, 2*X)
    X = np.where(X > -0.1, X, 2 * X)
    X = X/1.5
    return X


def tremalo(X, S, dep, typ, fs):
    l = 500000
    Y = np.zeros(len(X))
    for i in range(0,len(X),l):
        frek = fft.fft(np.append(X[i:i+l],np.zeros(5000)))
        max = 0
        for n in range(len(frek)):
            if frek[n] > max:
                max = frek[n]
                k = n
        f = k * len(frek) / fs
        #print(f)
        Y[i:i+l] = tremalo1(X[i:i+l], f * 5* 2**(1/12), dep, typ, fs)

    return Y


def pitc(X, D, fs):
    X = X - (((2*X)**2)-1)

    #Xfre = fft.fft(X)
    #Y = np.zeros(D + 1)
    #Y[D] = 1
    #Xny = scipy.signal.fftconvolve(Xfre[0:int(len(X)/2)], Y, mode='same')
    #Xny = np.hstack((Xny, np.flip(Xny,0)))
    #Y = fft.ifft(Xny)
    #return np.real(Y)
    return X


def reverb(X, Rx):
    Y = scipy.convolve(X, Rx, mode='same')
    return Y * (X.max()/Y.max())


fs, X = scipy.io.wavfile.read("piano.wav")
fs1, Rx = scipy.io.wavfile.read("reverb1.wav")


t = time.time()
X[:,0] = compresor(X[:,0])
X[:,1] = compresor(X[:,1])
#X[:,0] = pitc(X[:,0], 1000, fs)
#X[:,1] = pitc(X[:,1], 1000, fs)
#X[:,0] = reverb(X[:,0], Rx[:,0])
#X[:,1] = reverb(X[:,1], Rx[:,1])
#X[:,0] = bitkross(X[:,0], 3)
#X[:,1] = bitkross(X[:,1], 3)
#X[:,0] = chorusFlanger(X[:,0], 50, 0.25, 0.1, 1, 0.5, fs)
#X[:,1] = chorusFlanger(X[:,1], 50, 0.25, 0.1, 1, 0.5, fs)
#X[:,0] = reverbEko(X[:,0], 5, 1, 1, fs)
#X[:,1] = reverbEko(X[:,1], 5, 1, 1, fs)
#X[:,0] = reverbEko(X[:,0], 100, 1, 1, fs)
#X[:,1] = reverbEko(X[:,1], 100, 1, 1, fs)
#X[:,0] = softClipping(X[:,0], 10, 10)
#X[:,1] = softClipping(X[:,1], 10, 10)
#X[:,0] = tremalo(X[:,0], 5, 0.5, 1, fs)
#X[:,1] = tremalo(X[:,1], 5, 0.5, 1, fs)
#X[:,0] = hardClipping(X[:,0], 15, 25)
#X[:,1] = hardClipping(X[:,1], 15, 25)
#X = pongDelay(X, 200, 1, 2, fs)
#X = whawha(X, 2, 400, 300, 1.5, fs)
#print(X.max(), X.min())
plt.plot(X[:,0])
plt.show()

#time.sleep(5)
sa.play_buffer(X, 2, 2, fs)

print(time.time()-t)

time.sleep(10)



