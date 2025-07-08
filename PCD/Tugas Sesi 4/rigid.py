import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image
img = cv2.imread(r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg')
if img is None:
    print("Error: Gambar tidak bisa dibaca. Periksa path file.")
    exit()
h, w = img.shape[:2]

# Rigid transformation parameters
angle = 45  # Degrees
scale = 1.0  # No scaling
center = (w//2, h//2)  # Rotation center

# Create rigid transformation matrix
rigid_matrix = cv2.getRotationMatrix2D(center, angle, scale)

# Apply rigid transformation
rigid_img = cv2.warpAffine(img, rigid_matrix, (w, h))

# Convert from BGR to RGB for matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
rigid_img_rgb = cv2.cvtColor(rigid_img, cv2.COLOR_BGR2RGB)

# Show results using matplotlib
plt.figure(figsize=(10, 5))
plt.subplot(121), plt.imshow(img_rgb), plt.title("Original")
plt.subplot(122), plt.imshow(rigid_img_rgb), plt.title("Rigid Transformation")
plt.show()