import cv2
import numpy as np
from matplotlib import pyplot as plt

def median_filter(image_path, kernel_size=5):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Melakukan median filtering
    blurred = cv2.medianBlur(img, kernel_size)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(blurred, cmap='gray')
    plt.title(f'Median Filter (kernel={kernel_size})')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
median_filter('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')