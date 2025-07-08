import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image
img = cv2.imread(r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg')
if img is None:
    print("Error: Gambar tidak bisa dibaca. Periksa path file.")
    exit()
h, w = img.shape[:2]

# Translation parameters
tx, ty = 50, 30  # Pixel displacement

# Create translation matrix
translation_matrix = np.float32([
    [1, 0, tx],
    [0, 1, ty]
])

# Apply translation
translated_img = cv2.warpAffine(img, translation_matrix, (w, h))

# Convert from BGR to RGB for matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
translated_img_rgb = cv2.cvtColor(translated_img, cv2.COLOR_BGR2RGB)

# Show results using matplotlib
plt.figure(figsize=(10, 5))
plt.subplot(121), plt.imshow(img_rgb), plt.title("Original")
plt.subplot(122), plt.imshow(translated_img_rgb), plt.title(f"Translated (tx={tx}, ty={ty})")
plt.show()