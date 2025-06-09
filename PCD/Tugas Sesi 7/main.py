import cv2
import numpy as np
from matplotlib import pyplot as plt

def histogram_equalization(image_path):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Melakukan equalisasi histogram
    equ = cv2.equalizeHist(img)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(equ, cmap='gray')
    plt.title('Histogram Equalized')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
histogram_equalization('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')