import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image
img = cv2.imread(r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg')
if img is None:
    print("Error: Gambar tidak bisa dibaca. Periksa path file.")
    exit()
h, w = img.shape[:2]

# Define 3 source points
src_points = np.float32([
    [50, 50],
    [200, 50], 
    [50, 200]
])

# Define 3 corresponding destination points
dst_points = np.float32([
    [10, 100],
    [200, 50],
    [100, 250]
])

# Get affine transformation matrix
affine_matrix = cv2.getAffineTransform(src_points, dst_points)

# Apply affine transformation
affine_img = cv2.warpAffine(img, affine_matrix, (w, h))

plt.figure(figsize=(10,5))
plt.subplot(121), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title("Original")
plt.subplot(122), plt.imshow(cv2.cvtColor(affine_img, cv2.COLOR_BGR2RGB)), plt.title("Affine Transformation")
plt.show()

# Show results
# cv2.imshow("Original", img)
# cv2.imshow("Affine Transformation", affine_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()