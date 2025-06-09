import cv2
import numpy as np
from matplotlib import pyplot as plt

def gaussian_filter(image_path, kernel_size=5, sigma=1.5):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Melakukan Gaussian filtering
    blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(blurred, cmap='gray')
    plt.title(f'Gaussian Filter (kernel={kernel_size}, σ={sigma})')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
gaussian_filter('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')