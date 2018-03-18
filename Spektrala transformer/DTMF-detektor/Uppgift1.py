import numpy as np
import imageio
import scipy.signal
import matplotlib.pyplot as plt

im = np.mean(imageio.imread("U1.jpg"), axis=2)
#im = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,255,0,0],[0,0,0,0,0],[0,0,0,0,0]])
kernel = np.array([[1,1,1],[1,1,1],[1,1,1]])*(1/9)

ram = np.zeros(im.shape + np.array(2), im.dtype)
ram[1:-1,1:-1] = im


xl = len(im[0])
yl = len(im[:,0])

nim = []
for y in range(1,yl+1):
    nx =[]
    for x in range(1,xl+1):
        #print(ram[y-1:y+2,x-1:x+2])
        #print(np.sum(ram[y-1:y+2,x-1:x+2] * kernel))
        nx.append((np.sum(ram[y-1:y+2,x-1:x+2] * kernel)))
    nim.append(nx)
nim = np.array(nim)

im1 = scipy.signal.convolve2d(im, kernel)
im2 = scipy.signal.convolve(im, kernel)

fig = plt.figure()
a=fig.add_subplot(2,2,1)
plt.imshow(im, cmap='gray')
a.set_title('Orginal')
a=fig.add_subplot(2,2,2)
plt.imshow(nim, cmap='gray')
a.set_title('After')
a=fig.add_subplot(2,2,3)
plt.imshow(im1, cmap='gray')
a.set_title('convolve2d')
a=fig.add_subplot(2,2,4)
plt.imshow(im2, cmap='gray')
a.set_title('convolve')
plt.show()

