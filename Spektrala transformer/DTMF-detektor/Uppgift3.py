import numpy as np
import scipy.signal
import imageio
import matplotlib.pyplot as plt

im = np.mean(imageio.imread("teracotta-wall.jpg"), axis=2)

kernely = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
kernelx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

Gx = scipy.signal.convolve2d(im, kernelx, mode='same',boundary='wrap')
Gy = scipy.signal.convolve2d(im, kernely, mode='same', boundary='wrap')

G = (Gx**2 + Gy**2)**(1/2)

fig = plt.figure()
a=fig.add_subplot(2,2,1)
plt.imshow(im, cmap='gray')
a.set_title('Orginal')
a=fig.add_subplot(2,2,2)
plt.imshow(abs(Gx), cmap='gray')
a.set_title('Gx')
a=fig.add_subplot(2,2,3)
plt.imshow(Gy, cmap='gray')
a.set_title('Gy')
a=fig.add_subplot(2,2,4)
plt.imshow(G, cmap='gray')
a.set_title('G')
plt.show()