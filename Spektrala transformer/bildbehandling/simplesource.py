#Uppgift 3: Sammansättning och icke-statiska vokaler
import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt

fs = 16000

vOO  = np.array([ 300,   600,    2350,   3250 ])#rot
vO   = np.array([ 350,   700,    2600,   3200 ])#rott
vAOAO= np.array([ 400,   700,    2450,   3250 ])#rÂ
vAO  = np.array([ 500,   850,    2550,   3250 ])#rÂtt
vAA  = np.array([ 600,   950,    2550,   3300 ])#bar
vA   = np.array([ 750,   1250,   2500,   3350 ])#barr
vII  = np.array([ 250,   2200,   3150,   3750 ])#bil
vI   = np.array([ 350,   2150,   2750,   3500 ])#bill
vEE  = np.array([ 350,   2250,   2850,   3550 ])#deg
vE   = np.array([ 500,   1900,   2550,   3350 ])#v‰gg
vAE  = np.array([ 650,   1700,   2500,   3450 ])#herr
vYY  = np.array([ 250,   2050,   2700,   3300 ])#ny
vY   = np.array([ 300,   2000,   2400,   3250 ])#hytt
vOEOE= np.array([ 400,   1750,   2300,   3350 ])#fˆd
vOE  = np.array([ 550,   1550,   2450,   3300 ])#fˆdd
vOE3 = np.array([ 550,   1150,   2450,   3250 ])#fˆr
vUU  = np.array([ 300,   1650,   2250,   2250 ])#duk


def simplesource(F0):
#
# sawtooth_source - variable frequency sawtooth waveform generator 
# input:
#   F0 (1xN row vector) - time-varying frequency (normalized by fs)
    Ph = np.cumsum(F0)
    Z = 2*np.fmod(Ph,1.0)-1
    Y = np.diff(Z)<0
    Y = np.append(Y, [0])
    return Y.astype(float)


def formantfilter(F,BW,X):
    R = 1 - BW / 2

    X = np.append([0,0], X)
    Y = np.zeros(len(X))
    for i in range(2, len(X)):
        theta = 2 * np.pi * F[i-2]
        Y[i] = (1 - R ** 2) * np.sin(theta)*X[i] + 2 * R * np.cos(theta)*Y[i-1] - R ** 2 * Y[i-2]
    return Y[2:]


def diftonger(V1, V2, F1, F2, T, fs, BW):
    F0 = np.linspace(F1/fs, F2/fs, fs*T)
    X = simplesource(F0)
    vF1 = np.linspace(V1[0]/fs, V2[0]/fs, fs*T)
    vF2 = np.linspace(V1[1] / fs, V2[1] / fs, fs * T)
    vF3 = np.linspace(V1[2] / fs, V2[2] / fs, fs * T)
    vF4 = np.linspace(V1[3] / fs, V2[3] / fs, fs * T)
    Y = formantfilter(vF1, BW, X) + formantfilter(vF2, BW, X) + \
        formantfilter(vF3, BW, X)*0.7 + formantfilter(vF4, BW, X)*0.3
    return Y




Y = diftonger(vAE, vI, 100, 120, 0.5, fs, 0.05)
print(Y, len(Y), Y.max())
Y = np.int16(Y * 32767)
sa.play_buffer(Y, 1, 2, fs)

plt.plot(Y)
plt.show()

