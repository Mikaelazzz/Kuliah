import cv2
import numpy as np
from matplotlib import pyplot as plt

def canny_edge(image_path, low_threshold=50, high_threshold=150):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Melakukan Canny edge detection
    edges = cv2.Canny(img, low_threshold, high_threshold)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(edges, cmap='gray')
    plt.title(f'Canny Edge Detection ({low_threshold}, {high_threshold})')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
canny_edge('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')