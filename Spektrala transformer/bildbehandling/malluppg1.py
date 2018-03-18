#Uppgift 1: Statiska vokaler

import numpy as np
import scipy
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import math
import matplotlib.pyplot as plt
import simpleaudio as sa

fs,X = scipy.io.wavfile.read("source.wav")

def tvåpolsresonatorn(F,B,fs):
    # Bandbredd
    bb = B/fs
    # Polradien R följer av bandbredden
    R = 1 - bb / 2
    # Resonansfrekvensen, normaliserad (0.5 motsvarar nyquistfrekvensen)
    f = F/fs
    # Polvinkeln theta följer av resonansfrekvensen
    theta = 2 * np.pi * f
    # Filtrets nämnare
    A = [1, -2 * R * np.cos(theta), R ** 2]
    # Filtrets täljare
    B = [(1 - R ** 2) * np.sin(theta)]
    return scipy.signal.lfilter(B,A,X)

def formant(F, fs):
    B = np.array([50, 75, 100, 150])
    return tvåpolsresonatorn(F[0],B[0],fs)+tvåpolsresonatorn(F[1],B[1],fs)+tvåpolsresonatorn(F[2],B[2],fs)\
           +tvåpolsresonatorn(F[3],B[3],fs)


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


def plotHz():
    #Bandbredd
    bb = 0.05
    #Polradien R följer av bandbredden
    R = 1-bb/2
    #Resonansfrekvensen, normaliserad (0.5 motsvarar nyquistfrekvensen)
    f = 0.1
    #Polvinkeln theta följer av resonansfrekvensen
    theta = 2*np.pi*f
    #Filtrets nämnare
    A = [1, -2*R*np.cos(theta), R**2]
    #Filtrets täljare
    B = [(1-R**2)*np.sin(theta)]

    Xi = np.append([1], np.zeros(100-1 ))
    Y = scipy.signal.lfilter(B,A,X)
    Yi = scipy.signal.lfilter(B, A, Xi)
    w, h = signal.freqz(B,A)

    Y = np.int16(Y)
    sa.play_buffer(Y, 1, 2, fs)

    fig = plt.figure()
    a = fig.add_subplot(2, 1, 1)
    plt.plot(w/np.pi, abs(h))
    a.set_title('')
    a = fig.add_subplot(2, 1, 2)
    plt.stem(Yi)
    a.set_title('')
    plt.show()


if __name__ == '__main__':
    Y = formant(vE, fs)
    Y = np.int16(Y)
    sa.play_buffer(Y, 1, 2, fs)
    #scipy.io.wavfile.write("blo.wav", fs, Y)

    plotHz()

#Lägg till matris med formanter

