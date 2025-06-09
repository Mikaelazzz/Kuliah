import cv2
import numpy as np
from matplotlib import pyplot as plt

def kirsch_edge(image_path):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Mendefinisikan mask Kirsch
    masks = [
        np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]),   # N
        np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]]),   # NE
        np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),   # E
        np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]]),   # SE
        np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]),   # S
        np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]),   # SW
        np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),   # W
        np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]])    # NW
    ]
    
    # Melakukan konvolusi dengan semua mask
    max_edges = np.zeros_like(img, dtype=np.float32)
    for mask in masks:
        edges = cv2.filter2D(img.astype(np.float32), -1, mask)
        max_edges = np.maximum(max_edges, np.abs(edges))
    
    # Normalisasi
    kirsch = cv2.normalize(max_edges, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(kirsch, cmap='gray')
    plt.title('Kirsch Edge Detection')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
kirsch_edge('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')