import cv2
import numpy as np
from matplotlib import pyplot as plt

def prewitt_edge(image_path):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Mendefinisikan kernel Prewitt
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    
    # Melakukan konvolusi
    prewitt_x = cv2.filter2D(img, cv2.CV_64F, kernelx)
    prewitt_y = cv2.filter2D(img, cv2.CV_64F, kernely)
    
    # Mengkonversi ke nilai absolut dan menggabungkan
    abs_x = cv2.convertScaleAbs(prewitt_x)
    abs_y = cv2.convertScaleAbs(prewitt_y)
    prewitt = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(prewitt, cmap='gray')
    plt.title('Prewitt Edge Detection')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
prewitt_edge('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')