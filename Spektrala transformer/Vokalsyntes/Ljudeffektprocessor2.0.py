import numpy as np
import simpleaudio as sa
import scipy
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog


def chorusFlanger(X, D, f, md, a, b, fs):
    Y = np.zeros(len(X) + int(D + md))
    D = fs * D / 1000
    f = f / fs

    for i in range(len(X)):
        t = int(D * (1 + md * np.sin(2 * np.pi * f * i)))
        Y[i] = a * X[i] + b * X[i - t]

    return Y[0:len(X)]


def reverbEko(X, D, a, b, fs):
    D = int(fs * D / 1000)
    B = [b]
    A = np.zeros(D + 1)
    A[0] = 1
    A[D] = a
    Y = scipy.signal.lfilter(B, A, X)

    return Y


def softClipping(X, G):
    Xm = X.max()
    X = X / 32767 * G
    X = (X - X**3/3)
    X = np.where(X <= 2/3, X, 2/3)
    X = np.where(X >= -2/3, X, -2/3)
    X *= (Xm / X.max())
    return X


def hardClipping(X, G):
    Xm = X.max()
    X = X / 32767 * G
    Y = X
    Y = np.where(Y <= 1, Y, 1)
    Y = np.where(Y >= -1, Y, -1)
    Y *= Xm
    return Y


def formantfilter(X, F, BW):
    R = 1 - BW / 2

    X = np.append([0, 0], X)
    Y = np.zeros(len(X))
    for i in range(2, len(X)):
        theta = 2 * np.pi * F[i - 2]
        Y[i] = (1 - R ** 2) * np.sin(theta) * X[i] + 2 * R * np.cos(theta) * Y[i - 1] - R ** 2 * Y[i - 2]
    return Y[2:]


def bitkross(X, bitar):
    m = np.array([X.max(), X.min()])
    X = X/abs(m.max())
    X = X*((2**bitar/2)-0.9)
    X = np.floor(X)
    X = X/((2**bitar/2)-0.9)
    X = X*abs(m.max())
    return X


def reverb(X, Rx):
    Y = scipy.signal.fftconvolve(X, Rx)
    return (Y * (X.max()/Y.max()))[0:len(X)]


class Ljudeffektprocessor():
    def __init__(self):
        self.X = [0]
        self.X0 = [0]
        self.fs = 44100
        self.effekter = []
        self.file = "piano.wav"
        self.revfile = "reverb1.wav"
        self.nk = 2
        self.Rnk = 2
        self.loade()


    def loadFil(self):
        self.file = filedialog.askopenfilename()
        self.loade()

    def loadRev(self):
        self.revfile = filedialog.askopenfilename()

    def loade(self):
        self.fs, self.X = scipy.io.wavfile.read(self.file)
        self.fs, self.X0 = scipy.io.wavfile.read(self.file)

        # antal kanaler
        try:
            if len(self.X[0]) == 2:
                self.nk = 2
        except:
            self.nk = 1

        # effekter
        for i in self.effekter:
            if i == 0:
                self.delay(gui.delSlider1.get(), gui.delSlider2.get(), gui.delSlider3.get(), gui.delSlider4.get())
            elif i == 1:
                self.reverb(gui.revSlider1.get(), gui.revSlider2.get(), gui.revSlider3.get())
            elif i == 2:
                self.whawha(gui.whaSlider1.get(), gui.whaSlider2.get(), gui.whaSlider3.get(), gui.whaSlider1.get())
            elif i == 3:
                self.chorus_flanger(gui.cflSlider1.get(), gui.cflSlider2.get(), gui.cflSlider3.get(), gui.cflSlider5.get(), gui.cflSlider4.get())
            elif i == 4:
                self.distorsion(gui.disSlider1.get(), gui.disSlider2.get(), gui.disSlider3.get())
            elif i == 5:
                self.bitKross(gui.bitSlider.get())
            elif i == 6:
                self.reverb1()


    def spela(self, X):
        self.X = np.int16(self.X)
        if X == 1:
            sa.play_buffer(self.X0, self.nk, 2, self.fs)
        elif X == 2:
            sa.play_buffer(self.X, self.nk, 2, self.fs)

    def delay(self, D, a, b, mode=1):
        if self.nk == 2:
            self.X[:, 0] = reverbEko(self.X[:, 0], D, a, b, self.fs)
            self.X[:, 1] = reverbEko(self.X[:, 1], D, a, b, self.fs)
            if mode == 2:
                # pongdeley
                Dn = int(self.fs * D / 2000)
                Y = np.append(np.zeros(Dn), self.X[:, 1])
                self.X[:, 1] = Y[0:len(self.X[:, 1])]
        else:
            self.X = reverbEko(self.X, D, a, b, self.fs)

    def reverb(self, D, a, b):
        if self.nk == 2:
            self.X[:, 0] = reverbEko(self.X[:, 0], D, a, b, self.fs)
            self.X[:, 1] = reverbEko(self.X[:, 1], D, a, b, self.fs)
        else:
            self.X = reverbEko(self.X, D, a, b, self.fs)

    def whawha(self, S, Fm, dF, BW):
        T = np.array(range(len(self.X)))
        S = 2 * np.pi * S / self.fs
        F = Fm - dF * np.sin(S * T)
        if self.nk == 2:
            self.X[:, 0] = formantfilter(self.X[:, 0], F, BW)
            self.X[:, 1] = formantfilter(self.X[:, 1], F, BW)
        else:
            self.X = formantfilter(self.X, F, BW)

    def chorus_flanger(self, D, f, md, a, b):
        if self.nk == 2:
            self.X[:, 0] = chorusFlanger(self.X[:, 0], D, f, md, a, b, self.fs)
            self.X[:, 1] = chorusFlanger(self.X[:, 1], D, f, md, a, b, self.fs)
        else:
            self.X = chorusFlanger(self.X, D, f, md, a, b, self.fs)

    def distorsion(self, sc_G, hc_G, mode=1):
        if self.nk == 2:
            if mode == 1:
                self.X[:, 0] = softClipping(self.X[:, 0], sc_G)
                self.X[:, 1] = softClipping(self.X[:, 1], sc_G)
            elif mode == 2:
                self.X[:, 0] = hardClipping(self.X[:, 0], hc_G)
                self.X[:, 1] = hardClipping(self.X[:, 1], hc_G)
            elif mode == 3:
                self.X[:, 0] = softClipping(self.X[:, 0], sc_G)
                self.X[:, 1] = softClipping(self.X[:, 1], sc_G)
                self.X[:, 0] = hardClipping(self.X[:, 0], hc_G)
                self.X[:, 1] = hardClipping(self.X[:, 1], hc_G)
        else:
            if mode == 1:
                self.X = softClipping(self.X, sc_G)
            elif mode == 2:
                self.X = hardClipping(self.X, hc_G)
            elif mode == 3:
                self.X = softClipping(self.X, sc_G)
                self.X = hardClipping(self.X, hc_G)

    def bitKross(self, bitar):
        if self.nk == 2:
            self.X[:, 0] = bitkross(self.X[:, 0], bitar)
            self.X[:, 1] = bitkross(self.X[:, 1], bitar)
        else:
            self.X = bitkross(self.X, bitar)

    def reverb1(self):
        fs, Rx = scipy.io.wavfile.read(self.revfile)
        if self.nk == 2:
            Y = np.zeros((len(Rx[:,0]), len(Rx[0])))
            self.x = np.vstack((self.X, Y))
            self.X[:, 0] = reverb(self.X[:, 0], Rx[:, 0])
            self.X[:, 1] = reverb(self.X[:, 1], Rx[:, 1])
        else:
            self.X = reverb(self.X, Rx[:, 0])

    def plotLjud(self):
        if self.nk == 2:
            fig = plt.figure()
            fig.add_subplot(2, 2, 1)
            plt.plot(self.X[:, 0])
            fig.add_subplot(2, 2, 2)
            plt.plot(self.X[:, 1])
            fig.add_subplot(2, 2, 3)
            plt.plot(self.X0[:, 0])
            fig.add_subplot(2, 2, 4)
            plt.plot(self.X0[:, 1])
        else:
            fig = plt.figure()
            fig.add_subplot(2, 1, 1)
            plt.plot(self.X)
            fig.add_subplot(2, 1, 2)
            plt.plot(self.X0)
        plt.show()

def hello():
    pass


class GUI():
    def __init__(self, root):
        self.root = root

        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True, side=TOP)
        self.top_frame = Frame(self.main_frame)
        self.top_frame.pack(fill=BOTH, expand=False, side=TOP, padx=10, pady=10)

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=E.loadFil)
        filemenu.add_command(label="Save", command=hello)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Delay", command=self.delayGUI)
        editmenu.add_command(label="Reverb", command=self.reverbGUI)
        editmenu.add_command(label="Reverb1", command=self.reverb1GUI)
        editmenu.add_command(label="Wha-wha", command=self.whawhaGUI)
        editmenu.add_command(label="Chorus/Flanger", command=self.chorusFlangerGUI)
        editmenu.add_command(label="Distorsion", command=self.distorsionGUI)
        editmenu.add_command(label="Bitcrusher", command=self.bitkrossGUI)
        menubar.add_cascade(label="Add effect", menu=editmenu)

        root.config(menu=menubar)

        Button(self.top_frame, text="play 0", command=lambda X=1: E.spela(X)).pack(side=LEFT)
        Button(self.top_frame, text="play", command=lambda X=2: E.spela(X)).pack(side=LEFT)
        Button(self.top_frame, text="Load effects", command=E.loade).pack(side=LEFT)
        Button(self.top_frame, text="plot", command=E.plotLjud).pack(side=LEFT)

    def delayGUI(self):
        E.effekter.append(0)
        self.delay_frame = Frame(self.main_frame)
        self.delay_frame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)
        self.delX = Button(self.delay_frame, text='X', command=self.disDelGUI)
        self.delX.grid(row=0, column=3)
        l1 = Label(self.delay_frame, text="Delay").grid(row=0, column=0)
        l2 = Label(self.delay_frame, text="Del").grid(row=1, column=0)
        l3 = Label(self.delay_frame, text="Dec").grid(row=1, column=1)
        l4 = Label(self.delay_frame, text="Vol").grid(row=1, column=2)
        self.delSlider1 = Scale(self.delay_frame, length=179, from_=100, to=600, showvalue=1, resolution=1)
        self.delSlider1.grid(row=2, column=0)
        self.delSlider2 = Scale(self.delay_frame, length=179, from_=0, to=1, showvalue=0.01, resolution=0.01)
        self.delSlider2.grid(row=2, column=1)
        self.delSlider3 = Scale(self.delay_frame, length=179, from_=0, to=1, showvalue=0.01, resolution=0.01)
        self.delSlider3.grid(row=2, column=2)
        self.delSlider4 = Scale(self.delay_frame, length=40, from_=1, to=2, showvalue=1, resolution=1, orient=HORIZONTAL)
        self.delSlider4.grid(row=1, column=3)

    def disDelGUI(self):
        self.delay_frame.destroy()
        E.effekter.remove(0)

    def reverbGUI(self):
        E.effekter.append(1)
        self.reverb_frame = Frame(self.main_frame)
        self.reverb_frame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)
        self.revX = Button(self.reverb_frame, text='X', command=self.disRevGUI)
        self.revX.grid(row=0, column=3)
        l1 = Label(self.reverb_frame, text="Reverb").grid(row=0, column=0)
        l2 = Label(self.reverb_frame, text="Del").grid(row=1, column=0)
        l3 = Label(self.reverb_frame, text="Dec").grid(row=1, column=1)
        l4 = Label(self.reverb_frame, text="Vol").grid(row=1, column=2)
        self.revSlider1 = Scale(self.reverb_frame, length=200, from_=1, to=75, showvalue=1, resolution=1)
        self.revSlider1.grid(row=2, column=0)
        self.revSlider2 = Scale(self.reverb_frame, length=200, from_=0, to=1, showvalue=0.01, resolution=0.01)
        self.revSlider2.grid(row=2, column=1)
        self.revSlider3 = Scale(self.reverb_frame, length=200, from_=0, to=1, showvalue=0.01, resolution=0.01)
        self.revSlider3.grid(row=2, column=2)

    def disRevGUI(self):
        self.reverb_frame.destroy()
        E.effekter.remove(1)

    def whawhaGUI(self):
        E.effekter.append(2)
        self.wha_frame = Frame(self.main_frame)
        self.wha_frame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)
        self.whaX = Button(self.wha_frame, text='X', command=self.disWhaGUI)
        self.whaX.grid(row=0, column=4)
        l1 = Label(self.wha_frame, text="wha").grid(row=0, column=0)
        l2 = Label(self.wha_frame, text="Spe").grid(row=1, column=0)
        l3 = Label(self.wha_frame, text="mfre").grid(row=1, column=1)
        l4 = Label(self.wha_frame, text="dfre").grid(row=1, column=2)
        l4 = Label(self.wha_frame, text="bfre").grid(row=1, column=3)
        self.whaSlider1 = Scale(self.wha_frame, length=200, from_=0, to=3, showvalue=0.001, resolution=0.001)
        self.whaSlider1.grid(row=2, column=0)
        self.whaSlider2 = Scale(self.wha_frame, length=200, from_=50, to=1000, showvalue=1, resolution=1)
        self.whaSlider2.grid(row=2, column=1)
        self.whaSlider3 = Scale(self.wha_frame, length=200, from_=5, to=1000, showvalue=1, resolution=1)
        self.whaSlider3.grid(row=2, column=2)
        self.whaSlider4 = Scale(self.wha_frame, length=200, from_=0, to=1.99, showvalue=0.01, resolution=0.01)
        self.whaSlider4.grid(row=2, column=3)

    def disWhaGUI(self):
        self.wha_frame.destroy()
        E.effekter.remove(2)

    def chorusFlangerGUI(self):
        E.effekter.append(3)
        self.cfl_frame = Frame(self.main_frame)
        self.cfl_frame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)
        self.cflX = Button(self.cfl_frame, text='X', command=self.disCFlGUI)
        self.cflX.grid(row=0, column=5)
        l1 = Label(self.cfl_frame, text="Chorus/Flanger").grid(row=0, column=0, columnspan=2)
        l2 = Label(self.cfl_frame, text="Del").grid(row=1, column=0)
        l3 = Label(self.cfl_frame, text="fre").grid(row=1, column=1)
        l4 = Label(self.cfl_frame, text="effdep").grid(row=1, column=2)
        l5 = Label(self.cfl_frame, text="effV").grid(row=1, column=3)
        l6 = Label(self.cfl_frame, text="V").grid(row=1, column=4)
        self.cflSlider1 = Scale(self.cfl_frame, length=200, from_=1, to=100, showvalue=0.1, resolution=0.1)
        self.cflSlider1.grid(row=2, column=0)
        self.cflSlider2 = Scale(self.cfl_frame, length=200, from_=0, to=1, showvalue=0.01, resolution=0.01)
        self.cflSlider2.grid(row=2, column=1)
        self.cflSlider3 = Scale(self.cfl_frame, length=200, from_=0, to=1, showvalue=0.01, resolution=0.01)
        self.cflSlider3.grid(row=2, column=2)
        self.cflSlider5 = Scale(self.cfl_frame, length=200, from_=0, to=1, showvalue=0.01, resolution=0.01)
        self.cflSlider5.grid(row=2, column=4)
        self.cflSlider4 = Scale(self.cfl_frame, length=200, from_=0, to=1, showvalue=0.01, resolution=0.01)
        self.cflSlider4.grid(row=2, column=3)

    def disCFlGUI(self):
        self.cfl_frame.destroy()
        E.effekter.remove(3)

    def distorsionGUI(self):
        E.effekter.append(4)
        self.distorsion_frame = Frame(self.main_frame)
        self.distorsion_frame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)
        self.disX = Button(self.distorsion_frame, text='X', command=self.disDisGUI)
        self.disX.grid(row=0, column=5)
        l1 = Label(self.distorsion_frame, text="Distorsion").grid(row=0, column=0, columnspan=2)
        l2 = Label(self.distorsion_frame, text="SC").grid(row=1, column=0)
        l3 = Label(self.distorsion_frame, text="HC").grid(row=1, column=1)
        self.disSlider1 = Scale(self.distorsion_frame, length=179, from_=0, to=80, showvalue=0.1, resolution=0.1)
        self.disSlider1.grid(row=2, column=0)
        self.disSlider2 = Scale(self.distorsion_frame, length=179, from_=0, to=80, showvalue=0.1, resolution=0.1)
        self.disSlider2.grid(row=2, column=1)
        self.disSlider3 = Scale(self.distorsion_frame, length=40, from_=1, to=3, showvalue=1, resolution=1, orient=HORIZONTAL)
        self.disSlider3.grid(row=1, column=5)

    def disDisGUI(self):
        self.distorsion_frame.destroy()
        E.effekter.remove(4)

    def bitkrossGUI(self):
        E.effekter.append(5)
        self.bitkross_frame = Frame(self.main_frame)
        self.bitkross_frame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)
        self.bitX = Button(self.bitkross_frame, text='X', command=self.disBitGUI)
        self.bitX.grid(row=0, column=1)
        l1 = Label(self.bitkross_frame, text="Bitcrusher").grid(row=0, column=0)
        l2 = Label(self.bitkross_frame, text="Bits").grid(row=1, column=0)
        self.bitSlider = Scale(self.bitkross_frame, length=200, from_=16, to=1, showvalue=1, resolution=1)
        self.bitSlider.grid(row=2, column=0)

    def disBitGUI(self):
        self.bitkross_frame.destroy()
        E.effekter.remove(5)

    def reverb1GUI(self):
        E.effekter.append(6)
        self.rv1_frame = Frame(self.main_frame)
        self.rv1_frame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)
        self.bitX = Button(self.rv1_frame, text='X', command=self.disRv1GUI)
        self.bitX.grid(row=0, column=1)
        l1 = Label(self.rv1_frame, text="Reverb").grid(row=0, column=0)
        self.bitX = Button(self.rv1_frame, text='loade reverb', command=E.loadRev)
        self.bitX.grid(row=1, column=0)

    def disRv1GUI(self):
        self.rv1_frame.destroy()
        E.effekter.remove(6)

root = Tk()
E = Ljudeffektprocessor()
gui = GUI(root)
root.mainloop()
