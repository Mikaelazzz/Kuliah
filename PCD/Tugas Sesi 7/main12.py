import cv2
import numpy as np
from matplotlib import pyplot as plt

def robinson_edge(image_path):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Mendefinisikan mask Robinson
    masks = [
        np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),  # N
        np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]),   # NE
        np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]),    # E
        np.array([[2, 1, 0], [1, 0, -1], [0, -1, -2]]),    # SE
        np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]),    # S
        np.array([[0, -1, -2], [1, 0, -1], [2, 1, 0]]),    # SW
        np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),    # W
        np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])     # NW
    ]
    
    # Melakukan konvolusi dengan semua mask
    max_edges = np.zeros_like(img, dtype=np.float32)
    for mask in masks:
        edges = cv2.filter2D(img.astype(np.float32), -1, mask)
        max_edges = np.maximum(max_edges, np.abs(edges))
    
    # Normalisasi
    robinson = cv2.normalize(max_edges, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(robinson, cmap='gray')
    plt.title('Robinson Edge Detection')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
robinson_edge('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')