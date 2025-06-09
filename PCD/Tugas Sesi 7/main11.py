import cv2
import numpy as np
from matplotlib import pyplot as plt

def sobel_edge(image_path, ksize=3):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Melakukan Sobel edge detection
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Mengkonversi ke nilai absolut dan menggabungkan
    abs_sobelx = cv2.convertScaleAbs(sobelx)
    abs_sobely = cv2.convertScaleAbs(sobely)
    sobel = cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(sobel, cmap='gray')
    plt.title(f'Sobel Edge Detection (ksize={ksize})')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
sobel_edge('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')