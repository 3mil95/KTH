#Uppgift 2: En tidsvariabel resonator

import numpy as np
import scipy 
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import math
import matplotlib.pyplot as plt
import simpleaudio as sa


def formantfilter(F,BW,X):
    R = 1 - BW / 2

    Y = np.zeros(8000)
    for i in range(2,8000):
        theta = 2 * np.pi * F[i]
        Y[i] = (1 - R ** 2) * np.sin(theta)*X[i] +2 * R * np.cos(theta)*Y[i-1] - R ** 2 * Y[i-2]
    return Y
# formantfilter - time-varying two-pole resonator filter
#
# input:
#   F (1xN row vector)    - Time-varying resonance frequency (normalized by fs)
#   BW (real number)      - Constant bandwidth (normalized by fs)
#   X (1xN row vector)    - Input sequence
# output:
#   Y (1xN row vector)  - Output sequence

if __name__ == '__main__':
    X=np.random.rand(8000)
    F=np.linspace(0,0.5,8000)

    Y = formantfilter(F, 0.05, X)
    Y = np.int16(Y * 4000)
    sa.play_buffer(Y, 1, 2, 16000)

    w, h = signal.freqz(Y)
    plt.plot(abs(h))
    plt.show()