import numpy as np
import scipy.signal
import imageio
import matplotlib.pyplot as plt
import time


def gaussblur(im, N):
    x = np.array(range(N))
    N -= 1
    hx = np.array([(1/((2 * (N/6)**2 * np.pi)**(1/2)) * np.e ** -((((x) - (N/2)) ** 2)/(2*(N/6)**2)))])
    im1 = scipy.signal.convolve(im, hx, mode='same')
    return scipy.signal.convolve(im1, hx.T, mode='same')#.astype(int)


def gauss(im, N):
    X = np.linspace(int(-(N-1)/2),int((N-1)/2), N)
    K = []
    for y in X:
        Kx =[]
        for x in X:
            Kx.append(1/(2 * (2 * (N/6)**2 * np.pi)**(1/2)) * np.e**-((x**2 + y**2)/(2 * (N/6)**2)))
        K.append(Kx)
    K = np.array(K)

    return scipy.signal.convolve(im, K, mode='same')


if __name__ == '__main__':
    im = np.mean(imageio.imread("lynn-eyes-halftone.png"), axis=2)
    fig = plt.figure()
    a = fig.add_subplot(2, 2, 1)
    plt.imshow(im, cmap='gray')
    a.set_title('orginal')
    a = fig.add_subplot(2, 2, 2)
    plt.imshow(gauss(im, 9), cmap='gray')
    a.set_title('N=9, Loop')
    a = fig.add_subplot(2, 2, 3)
    plt.imshow(gaussblur(im, 9), cmap='gray')
    a.set_title('N=9')
    a = fig.add_subplot(2, 2, 4)
    plt.imshow(gaussblur(im, 19), cmap='gray')
    a.set_title('N=19')
    plt.show()

    T = time.time()
    gauss(im, 19)
    print(time.time()-T)
    T = time.time()
    gaussblur(im, 19)
    print(time.time() - T)



