import cv2
import numpy as np
from matplotlib import pyplot as plt

def harris_corner(image_path, block_size=2, ksize=3, k=0.04, threshold=0.01):
    # Membaca gambar
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    
    # Mendeteksi corner dengan Harris
    dst = cv2.cornerHarris(gray, block_size, ksize, k)
    
    # Hasil dilate untuk marking corner
    dst = cv2.dilate(dst, None)
    
    # Threshold untuk hasil optimal
    img[dst > threshold * dst.max()] = [0, 0, 255]
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Harris Corner Detection')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
harris_corner('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')