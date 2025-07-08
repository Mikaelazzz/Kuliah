import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image dengan path yang benar
img = cv2.imread(r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg')
if img is None:
    print("Error: Gambar tidak bisa dibaca. Periksa path file.")
    exit()

h, w = img.shape[:2]

# Define points dan lakukan transformasi
src_points = np.float32([[0,0], [w,0], [w,h], [0,h]])
dst_points = np.float32([[0,0], [w-100,50], [w-50,h-50], [50,h]])
projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
projective_img = cv2.warpPerspective(img, projective_matrix, (w,h))

# Tampilkan dengan matplotlib
plt.figure(figsize=(10,5))
plt.subplot(121), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title("Original")
plt.subplot(122), plt.imshow(cv2.cvtColor(projective_img, cv2.COLOR_BGR2RGB)), plt.title("Projective")
plt.show()

# Alternatif: Simpan ke file
# cv2.imwrite('original.jpg', img)
# cv2.imwrite('transformed.jpg', projective_img)