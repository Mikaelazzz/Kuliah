import numpy as np
import cv2
import matplotlib.pyplot as plt

def apply_fourier_filter(image_path, filter_type, radius=30, band_width=20):
    """
    Menerapkan filter frekuensi pada gambar menggunakan DFT 2D.
    
    Parameters:
        image_path (str): Path ke file gambar
        filter_type (str): 'lowpass', 'highpass', atau 'bandpass'
        radius (int): Radius untuk low/high-pass filter
        band_width (int): Lebar band untuk band-pass filter
    """
    
    # Baca gambar dan konversi ke grayscale
    img = cv2.imread(r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Gambar tidak dapat dibaca")
    
    # Lakukan Transformasi Fourier 2D
    dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20 * np.log(np.abs(dft_shift))
    
    # Buat filter berdasarkan jenis yang diminta
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols), np.uint8)
    
    if filter_type == 'lowpass':
        cv2.circle(mask, (ccol, crow), radius, 1, -1)
    elif filter_type == 'highpass':
        cv2.circle(mask, (ccol, crow), radius, 1, -1)
        mask = 1 - mask
    elif filter_type == 'bandpass':
        cv2.circle(mask, (ccol, crow), radius + band_width, 1, -1)
        cv2.circle(mask, (ccol, crow), radius, 0, -1)
    else:
        raise ValueError("Filter type harus 'lowpass', 'highpass', atau 'bandpass'")
    
    # Terapkan filter
    filtered_dft = dft_shift * mask
    
    # Transformasi balik ke domain spasial
    f_ishift = np.fft.ifftshift(filtered_dft)
    img_filtered = np.fft.ifft2(f_ishift)
    img_filtered = np.abs(img_filtered)
    
    # Normalisasi gambar hasil
    img_filtered = cv2.normalize(img_filtered, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # Tampilkan hasil
    plt.figure(figsize=(15, 10))
    
    plt.subplot(131), plt.imshow(img, cmap='gray')
    plt.title('Gambar Asli'), plt.xticks([]), plt.yticks([])
    
    plt.subplot(132), plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Spektrum Frekuensi'), plt.xticks([]), plt.yticks([])
    
    plt.subplot(133), plt.imshow(img_filtered, cmap='gray')
    plt.title(f'Hasil {filter_type} Filter'), plt.xticks([]), plt.yticks([])
    
    plt.tight_layout()
    plt.show()

# Contoh penggunaan
image_path = 'contoh_gambar.jpg'  # Ganti dengan path gambar Anda

# Low-pass filter (mempertahankan frekuensi rendah)
apply_fourier_filter(image_path, 'lowpass', radius=30)

# High-pass filter (mempertahankan frekuensi tinggi)
apply_fourier_filter(image_path, 'highpass', radius=30)

# Band-pass filter (mempertahankan frekuensi tertentu)
apply_fourier_filter(image_path, 'bandpass', radius=30, band_width=20)