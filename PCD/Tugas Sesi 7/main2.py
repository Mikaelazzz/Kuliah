import cv2
import numpy as np
from matplotlib import pyplot as plt

def rotate_image(image_path, angle):
    # Membaca gambar
    img = cv2.imread(image_path)
    
    # Mendapatkan dimensi gambar
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    
    # Melakukan rotasi
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
    plt.title(f'Rotated {angle}°')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
rotate_image('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg', 45)