import cv2
import numpy as np

path_gambar = r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg'

def ukur_ketajaman(path_gambar):
    # Membaca gambar dari path yang diberikan (bukan path hardcoded)
    img = cv2.imread(path_gambar, cv2.IMREAD_GRAYSCALE)
    
    # Periksa apakah gambar berhasil dibaca
    if img is None:
        print(f"Gagal membaca gambar dari {path_gambar}")
        return 0
    
    # Hitung ketajaman menggunakan Laplacian
    laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
    return laplacian  # Nilai tinggi = gambar tajam

# Contoh penggunaan:
if __name__ == "__main__":
    # Daftar path gambar yang akan diukur
    gambar_contoh = {
        'f2.8':  r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\Tugas 2\images.jpg',
        'f8':  r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\image-test.png',
        'f16':  r'E:\Back Up E\Tugas Kuliah Semester 4\PCD\images.jpg',
    }
    
    # Ukur ketajaman setiap gambar
    hasil_ketajaman = {}
    for nama, path in gambar_contoh.items():
        hasil = ukur_ketajaman(path)
        hasil_ketajaman[nama] = hasil
        print(f"Ketajaman {nama}: {hasil:.2f}")
    
    # Tampilkan hasil dalam bentuk dictionary
    print("\nHasil pengukuran ketajaman:")
    print(hasil_ketajaman)