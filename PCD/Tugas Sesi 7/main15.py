import cv2
import numpy as np
from matplotlib import pyplot as plt

def frequency_filters(image_path):
    # Membaca gambar
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Fourier Transform
    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    
    # Membuat filter
    rows, cols = img.shape
    crow, ccol = rows//2, cols//2
    
    # Low pass filter
    mask_low = np.zeros((rows, cols, 2), np.uint8)
    mask_low[crow-30:crow+30, ccol-30:ccol+30] = 1
    
    # High pass filter
    mask_high = np.ones((rows, cols, 2), np.uint8)
    mask_high[crow-15:crow+15, ccol-15:ccol+15] = 0
    
    # Band pass filter
    mask_band = np.zeros((rows, cols, 2), np.uint8)
    mask_band[crow-50:crow+50, ccol-50:ccol+50] = 1
    mask_band[crow-20:crow+20, ccol-20:ccol+20] = 0
    
    # Mengaplikasikan filter
    fshift_low = dft_shift * mask_low
    fshift_high = dft_shift * mask_high
    fshift_band = dft_shift * mask_band
    
    # Inverse Fourier Transform
    f_ishift_low = np.fft.ifftshift(fshift_low)
    img_back_low = cv2.idft(f_ishift_low)
    img_back_low = cv2.magnitude(img_back_low[:,:,0], img_back_low[:,:,1])
    
    f_ishift_high = np.fft.ifftshift(fshift_high)
    img_back_high = cv2.idft(f_ishift_high)
    img_back_high = cv2.magnitude(img_back_high[:,:,0], img_back_high[:,:,1])
    
    f_ishift_band = np.fft.ifftshift(fshift_band)
    img_back_band = cv2.idft(f_ishift_band)
    img_back_band = cv2.magnitude(img_back_band[:,:,0], img_back_band[:,:,1])
    
    # Normalisasi
    img_back_low = cv2.normalize(img_back_low, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    img_back_high = cv2.normalize(img_back_high, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    img_back_band = cv2.normalize(img_back_band, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # Menampilkan hasil
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(2, 2, 2)
    plt.imshow(img_back_low, cmap='gray')
    plt.title('Low Pass Filter')
    plt.axis('off')
    
    plt.subplot(2, 2, 3)
    plt.imshow(img_back_band, cmap='gray')
    plt.title('Band Pass Filter')
    plt.axis('off')
    
    plt.subplot(2, 2, 4)
    plt.imshow(img_back_high, cmap='gray')
    plt.title('High Pass Filter')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# Contoh penggunaan
frequency_filters('E:\Back Up E\Tugas Kuliah Semester 4\SD\learning\PCD\Tugas Sesi 7\img.jpeg')