import cv2
import numpy as np
import os

# Ganti dengan path absolut yang benar ke gambar Anda
image_path = r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg'

# 1. Verifikasi file ada
if not os.path.exists(image_path):
    print(f"ERROR: File tidak ditemukan di:\n{image_path}")
    exit()

# 2. Baca gambar
img = cv2.imread(image_path)

# 3. Cek apakah gambar berhasil dibaca
if img is None:
    print("ERROR: Gambar tidak bisa dibaca")
    print("Mungkin file corrupt atau format tidak didukung")
    exit()

# 4. Proses shearing
try:
    h, w = img.shape[:2]
    
    # Shearing horizontal
    shear_x = 0.3
    shear_matrix = np.float32([
        [1, shear_x, 0],
        [0, 1, 0]
    ])
    
    sheared_img = cv2.warpAffine(img, shear_matrix, (w, h))
    
    # 5. Tampilkan hasil dengan matplotlib (lebih reliable)
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 5))
    plt.subplot(121), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Original"), plt.axis('off')
    plt.subplot(122), plt.imshow(cv2.cvtColor(sheared_img, cv2.COLOR_BGR2RGB))
    plt.title("Shearing Transform"), plt.axis('off')
    plt.show()

except Exception as e:
    print(f"Error saat processing: {str(e)}")