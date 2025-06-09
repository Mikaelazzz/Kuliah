import cv2
import numpy as np
from matplotlib import pyplot as plt

def skew_image(image_path, angle):
    # Membaca gambar
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    
    # Menghitung transformasi affine untuk skewing
    pts1 = np.float32([[0,0], [w-1,0], [0,h-1]])
    pts2 = np.float32([[0,0], [w-1,0], [np.tan(np.radians(angle))*(h-1),h-1]])
    M = cv2.getAffineTransform(pts1, pts2)
    skewed = cv2.warpAffine(img, M, (w,h))
    
    # Menampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(skewed, cv2.COLOR_BGR2RGB))
    plt.title(f'Skewed {angle}°')
    plt.axis('off')
    
    plt.show()

# Contoh penggunaan
skew_image('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg', 15)