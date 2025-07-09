import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('./src/exam.jpg')
if image is None:
    raise FileNotFoundError('Gambar tidak ditemukan.')

if len(image.shape) == 3:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
else:
    gray = image

threshold_value = 180 
_, hot_area = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

thermal_colormap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

def pixel_to_temp(pixel_value, t_min=20, t_max=40):
    return t_min + (t_max - t_min) * (pixel_value / 255)

hot_pixels = gray[hot_area == 255]
if hot_pixels.size > 0:
    avg_pixel = np.mean(hot_pixels)
    est_temp = pixel_to_temp(avg_pixel)
    temp_text = f"Suhu Area Panas: {est_temp:.1f}°C"
else:
    temp_text = "Suhu Area Panas: -"

plt.figure(figsize=(15,5))
plt.subplot(1,3,1)
plt.title('Gambar Thermal Asli')
plt.axis('off')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.subplot(1,3,2)
plt.title('Segmentasi Area Panas')
plt.axis('off')
plt.imshow(hot_area, cmap='gray')
plt.subplot(1,3,3)
plt.title('Efek Thermal (Colormap)')
plt.axis('off')
plt.imshow(cv2.cvtColor(thermal_colormap, cv2.COLOR_BGR2RGB))

plt.text(10, 30, temp_text, color='white', fontsize=14, bbox=dict(facecolor='black', alpha=0.7))
plt.tight_layout()
plt.show()
