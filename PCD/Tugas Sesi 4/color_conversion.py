import cv2
import matplotlib.pyplot as plt
import numpy as np

# Load gambar
image = cv2.imread(r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg')
if image is None:
    print("Error: Gambar tidak bisa dibaca. Periksa path file.")
    exit()

# Konversi warna
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
ycrb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

# Konversi ke RGB untuk ditampilkan (kecuali grayscale)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Untuk menampilkan channel-channel terpisah
hsv_channels = [hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]]
lab_channels = [lab[:,:,0], lab[:,:,1], lab[:,:,2]]
ycrb_channels = [ycrb[:,:,0], ycrb[:,:,1], ycrb[:,:,2]]

# Normalisasi channel untuk tampilan yang lebih baik
def normalize_channel(channel):
    return cv2.normalize(channel, None, 0, 255, cv2.NORM_MINMAX)

# Tampilkan hasil
plt.figure(figsize=(15, 10))

# Gambar asli
plt.subplot(4, 4, 1), plt.imshow(image_rgb), plt.title("Original RGB")
plt.subplot(4, 4, 2), plt.imshow(gray, cmap='gray'), plt.title("Grayscale")

# Tampilkan channel HSV
plt.subplot(4, 4, 5), plt.imshow(normalize_channel(hsv_channels[0])), plt.title("HSV - H")
plt.subplot(4, 4, 6), plt.imshow(normalize_channel(hsv_channels[1])), plt.title("HSV - S")
plt.subplot(4, 4, 7), plt.imshow(normalize_channel(hsv_channels[2])), plt.title("HSV - V")

# Tampilkan channel LAB
plt.subplot(4, 4, 9), plt.imshow(normalize_channel(lab_channels[0])), plt.title("LAB - L")
plt.subplot(4, 4, 10), plt.imshow(normalize_channel(lab_channels[1])), plt.title("LAB - A")
plt.subplot(4, 4, 11), plt.imshow(normalize_channel(lab_channels[2])), plt.title("LAB - B")

# Tampilkan channel YCrCb
plt.subplot(4, 4, 13), plt.imshow(normalize_channel(ycrb_channels[0])), plt.title("YCrCb - Y")
plt.subplot(4, 4, 14), plt.imshow(normalize_channel(ycrb_channels[1])), plt.title("YCrCb - Cr")
plt.subplot(4, 4, 15), plt.imshow(normalize_channel(ycrb_channels[2])), plt.title("YCrCb - Cb")

plt.tight_layout()
plt.show()