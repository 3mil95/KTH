import numpy as np
import simpleaudio as sa
import time
from tkinter import *
import scipy.signal as sci
import threading
import matplotlib.pyplot as plt

"""fs_Hz = 16000


def wave(f_Hz, t_s):
    x = np.arange(int(fs_Hz * t_s))
    tone = np.sin(2 * np.pi * x * f_Hz / fs_Hz)
    return tone

def play():
    Hz = 150
    tone = wave(Hz , 1) *0.1
    tone += wave(2 * Hz, 1) * 0.1
    tone += wave(3 * Hz, 1) * 0.1
    tone += wave(4 * Hz, 1) * 0.1
    tone += wave(5 * Hz, 1) * 0.1
    tone += wave(6 * Hz, 1) * 0.1
    tone += wave(7 * Hz, 1) * 0.1
    tone += wave(8 * Hz, 1) * 0.1
    tone += wave(9 * Hz, 1) * 0.1

    A = [1, 2, 3]
    B = [1]
    tone1 = sci.lfilter(A, B, tone)
    A = [1, 2, 2]
    tone2 = sci.lfilter(A, B, tone)

    tone = (tone1 + tone2)/2
    tone *= 0.1
    tone = np.int16(tone * 32767)
    sa.play_buffer(tone, 1, 2, fs_Hz)

root = Tk()
Button(root, command=play).pack()
root.mainloop()"""

j = -1**0.5

w = np.linspace(0, np.pi, 100)
H = 1 - ((2**0.5)*(np.e ** (j*w))) + (np.e ** (j*2*w))
#H = 1-2**0.5*(np.cos(w)-j*np.sin(w))+np.cos(2*w)+j*np.sin(2*w)
H = abs(H)
plt.plot(w, H)
plt.show()

print(np.cos(np.pi/4))

Z = (1 + j)/(2**0.5)

print(Z**2-((2**0.5)*Z)+1)