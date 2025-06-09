import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import wiener

def wiener_filter(image_path, kernel_size=5, noise_var=0.1):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Membuat gambar buram terlebih dahulu
    blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    
    # Menambahkan noise
    noisy = blurred + np.random.normal(0, noise_var, blurred.shape) * 255
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    
    # Mengaplikasikan Wiener filter
    wiener_filtered = wiener(noisy, (kernel_size, kernel_size), noise_var)
    wiener_filtered = np.uint8(wiener_filtered)
    
    # Menampilkan hasil
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(noisy, cmap='gray')
    plt.title('Blurred + Noisy Image')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(wiener_filtered, cmap='gray')
    plt.title('Wiener Filtered')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# Contoh penggunaan
wiener_filter('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')