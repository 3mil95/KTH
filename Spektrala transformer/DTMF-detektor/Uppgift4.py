import numpy as np
import scipy.signal
import imageio
import matplotlib.pyplot as plt
import Uppgift2


im = np.mean(imageio.imread("lynn-eyes-halftone.png"), axis=2)
im = np.mean(imageio.imread("teracotta-wall.jpg"), axis=2)
#im = np.mean(scipy.misc.imread("U1.jpg"), axis=2)

lp_im = np.array(Uppgift2.gaussblur(im, 10))
print(lp_im)
ny_im = im - lp_im
#ny_im = abs(ny_im)

fig = plt.figure()
a = fig.add_subplot(3, 1, 1)
plt.imshow(im, cmap='gray')
a.set_title('orginal')
a = fig.add_subplot(3, 1, 2)
plt.imshow(ny_im, cmap='gray')
a.set_title('N=5')
a = fig.add_subplot(3, 1, 3)
plt.imshow(lp_im, cmap='gray')
plt.show()

