import cv2
import numpy as np
import os
import matplotlib.pyplot as plt  # Untuk alternatif display

# Ganti dengan path lengkap ke gambar Anda
image_path = r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg'

print(f"Mencoba membuka file di: {image_path}")

if not os.path.exists(image_path):
    print(f"ERROR: File tidak ditemukan di:\n{image_path}")
    exit()


img = cv2.imread(image_path)

if img is None:
    print("ERROR: Gambar tidak bisa dibaca")
    print("Mungkin file corrupt atau format tidak didukung")
    exit()

try:
    # Scaling ke ukuran tertentu (400x300)
    resized = cv2.resize(img, (400, 300), interpolation=cv2.INTER_AREA)
    
    # Scaling dengan faktor (1.5x)
    scaled = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    
    # Konversi BGR ke RGB untuk matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    scaled_rgb = cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB)
    
    # Tampilkan semua hasil
    plt.figure(figsize=(15, 5))
    
    plt.subplot(131), plt.imshow(img_rgb)
    plt.title(f"Original\n{img.shape[1]}x{img.shape[0]}"), plt.axis('off')
    
    plt.subplot(132), plt.imshow(resized_rgb)
    plt.title(f"Resized 400x300\n{resized.shape[1]}x{resized.shape[0]}"), plt.axis('off')
    
    plt.subplot(133), plt.imshow(scaled_rgb)
    plt.title(f"Scaled 1.5x\n{scaled.shape[1]}x{scaled.shape[0]}"), plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    cv2.imwrite('resized_result.jpg', resized)
    cv2.imwrite('scaled_result.jpg', scaled)
    print("\nHasil telah disimpan sebagai:")
    print("- resized_result.jpg")
    print("- scaled_result.jpg")

except Exception as e:
    print(f"\nError selama pemrosesan: {str(e)}")