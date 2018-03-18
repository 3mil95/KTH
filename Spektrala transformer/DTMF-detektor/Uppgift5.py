import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import imageio

def gauss(N):
    X = np.linspace(int(-(N-1)/2),int((N-1)/2), N)
    K = []
    for y in X:
        Kx =[]
        for x in X:
            Kx.append(1/(2 * (2 * (N/6)**2 * np.pi)**(1/2)) * np.e**-((x**2 + y**2)/(2 * (N/6)**2)))
        K.append(Kx)
    return np.array(K)


im = np.mean(imageio.imread("lynn-eyes-halftone.png"), axis=2)
im = np.mean(imageio.imread("teracotta-wall.jpg"), axis=2)
freq = np.fft.fft2(im)
freq = np.fft.fftshift(freq)
R = 10

KS = np.ones((2*R+1,2*R+1))
KM = R
for n1 in range(R*2+1):
    for n2 in range(R * 2+1):
        if ((n2-KM)**2 + (n1-KM)**2)**0.5 <= R:
            KS[n1,n2] = 0

#KS = gauss(2*R + 1)
K = np.ones((len(im[:,0]),len(im[0])))
K[int(len(im[:,0])/2-R-1):int(len(im[:,0])/2+R), int(len(im[0])/2-R-1):int(len(im[0])/2+R)] = KS

freq *= K

plt.imshow(np.log(abs(freq)), cmap='gray')
plt.show()


freq = np.fft.ifft2(np.fft.fftshift(freq))
freq = abs(freq)


plt.imshow(freq, cmap='gray')
plt.show()