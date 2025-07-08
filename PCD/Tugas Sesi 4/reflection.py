import cv2
import os
import matplotlib.pyplot as plt

# Path gambar - GANTI DENGAN PATH ANDA
image_path = r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg'

# Cek file exist
if not os.path.exists(image_path):
    print(f"ERROR: File tidak ditemukan di {image_path}")
    exit()

# Baca gambar
img = cv2.imread(image_path)

if img is None:
    print("ERROR: Gambar tidak bisa dibaca")
    print("Mungkin file corrupt atau format tidak didukung")
    exit()

# Reflection
try:
    flipped = cv2.flip(img, 1)  # 1=horizontal, 0=vertical, -1=keduanya
    
    # Tampilkan dengan matplotlib
    plt.figure(figsize=(10,5))
    plt.subplot(121), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Original"), plt.axis('off')
    plt.subplot(122), plt.imshow(cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB))
    plt.title("Reflected"), plt.axis('off')
    plt.show()

    # Alternatif: Simpan ke file
    # cv2.imwrite('reflected.jpg', flipped)
    # print("Hasil disimpan sebagai 'reflected.jpg'")

except Exception as e:
    print(f"Error saat processing: {str(e)}")