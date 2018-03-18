import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.misc
import imageio

# Wheight matrix for jpeg
W = np.array(np.mat('16 11 10 16 24 40 51 61; 12 12 14 19 26 58 60 55; 14 13 16 24 40 57 69 56; 14 17 22 29 51 87 80 62; 18 22 37 56 68 109 103 77; 24 35 55 64 81 104 113 92; 49 64 78 87 103 121 120 101; 72 92 95 98 112 100 103 99'), dtype=float)

# Function: dct_basis for calculating dct-base-vector matrix
# Input: m (positive integer) - Basis vector length
# Output: T (mxm matrix) - DCT basis matrix, each column: basis vector
def dct_basis(m):
    # Initialize a matrix
    T = []
    # Fill it up ackording to equations in instructions
    for p in range(m):
        ny_row = []
        for q in range(m):
            ny_row.append(((2/m)**0.5)*(np.cos((math.pi*(2*p+1)*q)/(2*m))))
        T.append((ny_row))
    T = np.array(T)
    T[:, 0] = (1/(m)**0.5)
    return T


# Function: jpeg_encode. Encode image using block-by-block DCT-coefficients
# Input: I (nxm matrix) - Input image
# Output: C (nxm matrix) - DCT coefficient matrix
# Parameters: bs - blocksize
def jpeg_encode(I, DCT, com=0):
    # Initialize a matrix the same size as I
    C = np.zeros((len(I[0]), len(I[:,0])))
    # Divide into submatrices and apply matrix operations
    bs = 8
    for p in range(0, math.floor(I.shape[0] / bs)):
        for q in range(0, math.floor(I.shape[1] / bs)):
            Isub = I[p*bs: (p+1)*bs, q*bs: (q+1)*bs]
            Isub = Isub - 128*np.ones((bs, bs))
            #Put matrix operation under this line
            Csub = np.matmul(DCT.T, np.matmul(Isub, DCT))
            Csub = (Csub/ (W*com)).astype(int)
            ###
            C[p*bs: (p+1)*bs, q*bs: (q+1)*bs] = Csub
    return C


# Input: C (nxm matrix) - DCT transform matrix
# Output: I (nxm matrix) - Output image
def jpeg_decode(C, DCT, com=0):
    # Initialize a matrix the same size as C
    I = np.zeros((len(C[0]), len(C[:,0])))
    # Divide into submatrices and iteratively apply matrix operations
    bs = 8
    for p in range(0, math.floor(C.shape[0] / bs)):
        for q in range(0, math.floor(C.shape[1] / bs)):
            Csub = C[p*bs: (p+1)*bs, q*bs: (q+1)*bs]
            #Put matrix operation under this line
            Csub = (Csub * W)*com
            Isub = np.matmul(DCT, np.matmul(Csub, DCT.T))
            ###
            Isub = Isub + 128*np.ones((bs, bs))
            I[p*bs: (p+1)*bs, q*bs: (q+1)*bs] = Isub
    return I


def jprg(I, com=1 ,bs=8):
    DCT = dct_basis(bs)
    C = jpeg_encode(I, DCT, com)
    I = jpeg_decode(C, DCT, com)
    return I


def jpeg_ferg(I, com=[1,1,1]):
    R = I[:, :, 0]
    G = I[:, :, 1]
    B = I[:, :, 2]

    I = np.zeros((len(I[:, :, 0]), len(I[0]), len(I[0, 0])))

    Y = 0.299 * R + 0.587 * G + 0.114 * B
    U = -0.147 * R - 0.289 * G + 0.436 * B
    V = 0.615 * R - 0.515 * G - 0.100 * B

    Y = jprg(Y, com[0])
    U = jprg(U, com[1])
    V = jprg(V, com[2])

    R = Y + 1.13983 * V
    G = Y - 0.39465 * U - 0.5806 * V
    B = Y + 2.03211 * U

    I[:, :, 0] = R
    I[:, :, 1] = G
    I[:, :, 2] = B

    I = np.array(I.astype(int), dtype='uint8')
    return I


if __name__ == '__main__':
    im = imageio.imread('imageio:chelsea.png')
    I = im[0:296, 0:296]

    I2 = jpeg_ferg(I)
    I3 = jpeg_ferg(I, [5,10,10])
    I4 = jpeg_ferg(I, [5,1,1])

    fig = plt.figure()
    a = fig.add_subplot(2, 2, 1)
    plt.imshow(I, cmap='gray')
    a.set_title('orginal')
    a = fig.add_subplot(2, 2, 2)
    plt.imshow(I2)
    a.set_title('1,1,1')
    a = fig.add_subplot(2, 2, 3)
    plt.imshow(I3)
    a.set_title('1,2,3')
    a = fig.add_subplot(2, 2, 4)
    plt.imshow(I4, cmap='gray')
    a.set_title('5,1,1')
    plt.show()
