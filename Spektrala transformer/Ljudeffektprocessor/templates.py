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
    pass

def dct_test():
    m = 8
    T = dct_basis(m)
    I = np.ones((m, m))
    #I[:,1::2] = -1
    #I = np.eye(m)
    C = np.matmul(T.T, np.matmul(I,T))
    plt.imshow(C, cmap='gray')
    plt.show()
    fig = plt.figure()

    for p in range(m):
        for q in range(m):
            C = np.zeros((m, m))
            C[p,q] = 255
            I = np.matmul(T.T, C)
            I = np.matmul(I, T)
            a = fig.add_subplot(m, m, q+p*m+1)
            plt.imshow(I, cmap='gray')
            #a.set_title(q+p*m+1)
    plt.show()


# Function: jpeg_encode. Encode image using block-by-block DCT-coefficients
# Input: I (nxm matrix) - Input image
# Output: C (nxm matrix) - DCT coefficient matrix
# Parameters: bs - blocksize
def jpeg_encode(I, com=0):
    # Initialize a matrix the same size as I
    C = np.zeros((len(I[0]), len(I[:,0])))
    # Divide into submatrices and apply matrix operations
    bs = 8
    for p in range(0, math.floor(I.shape[0] / bs)):
        for q in range(0, math.floor(I.shape[1] / bs)):
            Isub = I[p*bs: (p+1)*bs, q*bs: (q+1)*bs]
            Isub = Isub - 128*np.ones((bs, bs))
            #Put matrix operation under this line
            Csub = np.matmul(dct_basis(bs).T, np.matmul(Isub,dct_basis(bs)))
            Csub = kvantisering(Csub, com)
            ###
            C[p*bs: (p+1)*bs, q*bs: (q+1)*bs] = Csub
    return C


def test_jpeg_encode():
    #I = np.mean(scipy.misc.imread("uggla2.tif"), axis=2)
    I = imageio.imread("uggla2.tif")

    C = jpeg_encode(I)

    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1)
    plt.imshow(I, cmap='gray')
    a.set_title('I')
    a = fig.add_subplot(1, 2, 2)
    plt.imshow(C, cmap='gray')
    a.set_title('C')
    plt.show()


# Input: C (nxm matrix) - DCT transform matrix
# Output: I (nxm matrix) - Output image
def jpeg_decode(C, com=0):
    # Initialize a matrix the same size as C
    I = np.zeros((len(C[0]), len(C[:,0])))
    # Divide into submatrices and iteratively apply matrix operations
    bs = 8
    for p in range(0, math.floor(C.shape[0] / bs)):
        for q in range(0, math.floor(C.shape[1] / bs)):
            Csub = C[p*bs: (p+1)*bs, q*bs: (q+1)*bs]
            #Put matrix operation under this line
            #Csub = (Csub * W)*com
            Isub = np.matmul(dct_basis(bs), np.matmul(Csub, dct_basis(bs).T))
            ###
            Isub = Isub + 128*np.ones((bs, bs))
            I[p*bs: (p+1)*bs, q*bs: (q+1)*bs] = Isub
    return I

def test_jpeg_decode():
    I = imageio.imread("uggla2.tif")

    C = jpeg_encode(I, 1)
    I2 = jpeg_decode(C, 1)

    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1)
    plt.imshow(I, cmap='gray')
    a.set_title('I')
    a = fig.add_subplot(1, 2, 2)
    plt.imshow(I2, cmap='gray')
    a.set_title('I2')
    plt.show()


def kvantisering(Csub, com):

    #Csub = np.where(Csub < Csub.max(), 0, Csub)

    N = np.zeros((8,8))
    N[0,0:4] = 1
    N[1, 0:3] = 1
    N[2, 0:2] = 1
    N[3, 0:1] = 1
    Csub = Csub*N
    #Csub = np.trunc(Csub)
    Csub = Csub/(W*com)
    Csub = Csub.astype(int)
    #print(np.count_nonzero(Csub))
    return Csub


def farg_jpeg():
    I = imageio.imread("Bild.jpg")
    #I = imageio.imread("uggla.tif")
    im = imageio.imread('imageio:chelsea.png')
    I = im[0:296,0:296]

    R = I[:,:,0]
    G = I[:,:,1]
    B = I[:,:,2]

    N_I = np.zeros((len(I[:,:,0]), len(I[0]), len(I[0,0])))

    Y = 0.299 * R + 0.587 * G + 0.114 * B
    U = -0.147 * R -0.289 * G + 0.436 *B
    V = 0.615 * R -0.515 * G - 0.100 *B

    Ycom = 1
    Ucom = 1
    Vcom = 1

    Y = jpeg_encode(Y, Ycom)
    U = jpeg_encode(U, Ucom)
    V = jpeg_encode(V, Vcom)

    Y = jpeg_decode(Y, Ycom)
    U = jpeg_decode(U, Ucom)
    V = jpeg_decode(V, Vcom)

    R = Y + 1.13983*V
    G = Y -0.39465*U -0.5806*V
    B = Y + 2.03211*U
    N_I[:,:,0] = R
    N_I[:, :, 1] = G
    N_I[:, :, 2] = B
    N_I = np.array(N_I.astype(int), dtype='uint8')
    #N_I = np.array(N_I.astype(int))
    fig = plt.figure()
    a = fig.add_subplot(2, 2, 1)
    plt.imshow(I)
    a.set_title('orginal')
    a = fig.add_subplot(2, 2, 2)
    plt.imshow(N_I)
    a.set_title('N=5')
    plt.show()
    pass


if __name__ == '__main__':
    # U1
    dct_test()
    # U2
    #test_jpeg_encode()
    # U3, U4
    #test_jpeg_decode()
    # U5
    #farg_jpeg()
    pass