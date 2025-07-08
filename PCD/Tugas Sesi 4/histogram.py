import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load gambar (untuk warna)
image = cv2.imread(r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg')

if image is None:
    print("Error: Gambar tidak bisa dibaca. Periksa path file.")
    exit()

# Cek apakah gambar grayscale atau warna
is_color = len(image.shape) == 3 and image.shape[2] == 3

plt.figure(figsize=(10, 5))

if is_color:
    # Hitung histogram untuk gambar warna
    colors = ('b', 'g', 'r')
    for i, col in enumerate(colors):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=col, label=f'Channel {col.upper()}')
    plt.title("Histogram Warna (RGB)")
else:
    # Hitung histogram untuk gambar grayscale
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    plt.plot(hist, color='black')
    plt.title("Histogram Grayscale")

plt.xlabel("Intensitas Pixel")
plt.ylabel("Frekuensi")
plt.xlim([0, 256])
if is_color:
    plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()