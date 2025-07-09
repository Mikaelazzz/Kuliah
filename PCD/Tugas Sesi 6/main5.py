import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import radon, iradon
from skimage import data
from skimage.feature import peak_local_max
from skimage.draw import line
from skimage.transform import probabilistic_hough_line

# Load or create an image with pronounced straight lines
image = data.checkerboard()  # Example image (replace with your own)
image = plt.imread(r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg')  # Uncomment to load your image

# Generate synthetic image with lines if needed
def create_line_image(size=200):
    img = np.zeros((size, size))
    rr, cc = line(50, 30, 150, 180)  # Line 1
    img[rr, cc] = 1
    rr, cc = line(20, 100, 180, 80)   # Line 2
    img[rr, cc] = 1
    return img

image = create_line_image()

# Perform Radon transform
theta = np.linspace(0., 180., max(image.shape), endpoint=False)
sinogram = radon(image, theta=theta)

# Find peaks in Radon transform (potential lines)
peaks = peak_local_max(sinogram, threshold_abs=0.8*np.max(sinogram),
                       min_distance=20, num_peaks=4)

# Convert peaks to line parameters
detected_lines = []
for peak in peaks:
    r, t = peak
    angle = theta[t]
    distance = r - sinogram.shape[0]//2
    detected_lines.append((distance, angle))

# Visualize results
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Original image with ground truth lines (for synthetic image)
ax1.imshow(image, cmap='gray')
ax1.set_title('Original Image')
ax1.set_axis_off()

# Radon transform with peaks marked
ax2.imshow(sinogram, cmap='hot', extent=(0, 180, -sinogram.shape[0]//2, sinogram.shape[0]//2),
           aspect='auto')
ax2.plot(theta[peaks[:, 1]], peaks[:, 0] - sinogram.shape[0]//2, 'ro')
ax2.set_title('Radon Transform (Sinogram)')
ax2.set_xlabel('Angle (deg)')
ax2.set_ylabel('Projection position (pixels)')

# Original image with detected lines
ax3.imshow(image, cmap='gray')
ax3.set_title('Detected Lines')
ax3.set_axis_off()

for d, theta in detected_lines:
    a = np.cos(np.deg2rad(theta))
    b = np.sin(np.deg2rad(theta))
    x0 = a*d
    y0 = b*d
    x1 = x0 + 1000*(-b)
    y1 = y0 + 1000*(a)
    ax3.plot([x0, x1], [y0, y1], '-r', linewidth=2)

plt.tight_layout()
plt.show()

# Compare with probabilistic Hough transform for verification
hough_lines = probabilistic_hough_line(image, threshold=10, line_length=10,
                                     line_gap=5)

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(image, cmap='gray')
for line_coords in hough_lines:
    ax.plot(*zip(*line_coords), '-g', linewidth=2)
ax.set_title('Probabilistic Hough Lines')
ax.set_axis_off()
plt.show()