import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception('Webcam tidak terdeteksi.')

threshold_value = 180 

plt.ion() 
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

def pixel_to_temp(pixel_value, t_min=20, t_max=40):
    return t_min + (t_max - t_min) * (pixel_value / 255)

while True:
    ret, frame = cap.read()
    if not ret:
        print('Gagal mengambil frame dari webcam')
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, hot_area = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    hot_pixels = gray[hot_area == 255]
    if hot_pixels.size > 0:
        avg_pixel = np.mean(hot_pixels)
        est_temp = pixel_to_temp(avg_pixel)
        temp_text = f"Suhu Area Panas: {est_temp:.1f}°C"
    else:
        temp_text = "Suhu Area Panas: -"

    thermal_colormap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    mask_colored = cv2.applyColorMap(hot_area, cv2.COLORMAP_JET)
    combined = cv2.addWeighted(frame, 0.7, mask_colored, 0.3, 0)

    combined_disp = combined.copy()
    cv2.putText(combined_disp, temp_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

    axs[0].clear()
    axs[1].clear()
    axs[2].clear()
    axs[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    axs[0].set_title('Webcam')
    axs[0].axis('off')
    axs[1].imshow(hot_area, cmap='gray')
    axs[1].set_title('Segmentasi Area Panas')
    axs[1].axis('off')
    axs[2].imshow(cv2.cvtColor(thermal_colormap, cv2.COLOR_BGR2RGB))
    axs[2].set_title('Efek Thermal (Colormap)')
    axs[2].axis('off')
    axs[2].text(10, 30, temp_text, color='white', fontsize=14, bbox=dict(facecolor='black', alpha=0.7))
    plt.pause(0.001)


cap.release()
plt.ioff()
plt.show()
