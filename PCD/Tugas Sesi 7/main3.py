import cv2
import numpy as np
from matplotlib import pyplot as plt

def scale_image(image_path, scale_factor):
    # Membaca gambar
    img = cv2.imread(image_path)
    
    # Melakukan perubahan skala
    width = int(img.shape[1] * scale_factor)
    height = int(img.shape[0] * scale_factor)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    plt.title(f'Scaled {scale_factor}x')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
scale_image('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg', 0.5)