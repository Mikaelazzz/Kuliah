import numpy as np
import matplotlib.pyplot as plt

def dft_1d(x):
    """
    Menghitung Transformasi Fourier Diskrit 1D dari sinyal input x.
    
    Parameter:
    x (array_like): Sinyal input (array 1D)
    
    Mengembalikan:
    complex ndarray: DFT dari sinyal input
    """
    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    return np.dot(e, x)

# Fungsi sampel untuk pengujian
def buat_sinyal(jenis_sinyal, N=64):
    """Membuat sinyal sampel untuk pengujian"""
    n = np.arange(N)
    if jenis_sinyal == 'sinus':
        return np.sin(2 * np.pi * n / N * 4)  # 4 siklus
    elif jenis_sinyal == 'cosinus':
        return np.cos(2 * np.pi * n / N * 2)  # 2 siklus
    elif jenis_sinyal == 'kotak':
        return np.where(n < N/2, 1, -1)
    elif jenis_sinyal == 'impuls':
        sinyal = np.zeros(N)
        sinyal[N//2] = 1
        return sinyal
    elif jenis_sinyal == 'acak':
        return np.random.randn(N)
    else:
        raise ValueError("Jenis sinyal tidak dikenali")

# Pengujian dan visualisasi
jenis_sinyal = ['sinus', 'cosinus', 'kotak', 'impuls', 'acak']
N = 64

plt.figure(figsize=(15, 10))

for i, jenis in enumerate(jenis_sinyal):
    # Membuat sinyal
    x = buat_sinyal(jenis, N)
    
    # Menghitung DFT
    X = dft_1d(x)
    
    # Plotting
    plt.subplot(len(jenis_sinyal), 3, i*3 + 1)
    plt.plot(x)
    plt.title(f'Gelombang {jenis}')
    plt.xlabel('Sampel')
    plt.ylabel('Amplitudo')
    
    plt.subplot(len(jenis_sinyal), 3, i*3 + 2)
    plt.plot(np.abs(X))
    plt.title('Spektrum Magnitudo')
    plt.xlabel('Bin frekuensi')
    plt.ylabel('Magnitudo')
    
    plt.subplot(len(jenis_sinyal), 3, i*3 + 3)
    plt.plot(np.angle(X))
    plt.title('Spektrum Fase')
    plt.xlabel('Bin frekuensi')
    plt.ylabel('Fase (radian)')

plt.tight_layout()
plt.show()