import numpy as np
import cv2
import matplotlib.pyplot as plt

def analisis_fourier(gambar):
    """Melakukan transformasi Fourier dan visualisasi"""
    # Konversi ke grayscale jika perlu
    if len(gambar.shape) > 2:
        gambar = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
    
    # Transformasi Fourier
    dft = np.fft.fft2(gambar)
    dft_shift = np.fft.fftshift(dft)
    spektrum = 20*np.log(np.abs(dft_shift))
    
    # Visualisasi
    plt.figure(figsize=(12, 6))
    plt.subplot(121), plt.imshow(gambar, cmap='gray')
    plt.title('Gambar Asli'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(spektrum, cmap='gray')
    plt.title('Spektrum Fourier'), plt.xticks([]), plt.yticks([])
    plt.show()
    
    return dft_shift

# Membuat gambar sederhana
ukuran = 256
gambar_sinus = np.zeros((ukuran, ukuran))
for x in range(ukuran):
    for y in range(ukuran):
        gambar_sinus[x,y] = 128 + 100*np.sin(2*np.pi*x/32)

gambar_kotak = np.zeros((ukuran, ukuran))
gambar_kotak[80:180, 80:180] = 255

gambar_diagonal = np.zeros((ukuran, ukuran))
for x in range(ukuran):
    for y in range(ukuran):
        if abs(x-y) < 10:
            gambar_diagonal[x,y] = 255

# Analisis gambar
print("Analisis Gambar Sinus:")
dft_sinus = analisis_fourier(gambar_sinus)

print("\nAnalisis Gambar Kotak:")
dft_kotak = analisis_fourier(gambar_kotak)

print("\nAnalisis Garis Diagonal:")
dft_diagonal = analisis_fourier(gambar_diagonal)