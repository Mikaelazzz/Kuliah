# Thermal Camera Segmentation Hot Area

Vincentius Johanes Lwie Jaya // 233408010

## Langkah Awal (Wajib Dibaca!)

### 1. Install Python
- Download Python versi 3.9 atau 3.10 dari https://www.python.org/downloads/
- Saat instalasi, centang "Add Python to PATH" agar Python bisa dijalankan dari Command Prompt.

### 2. Buka Command Prompt
- Klik kanan di folder project ini (tempat file thermal.py, thermalive.py, thermalapp.py berada), lalu pilih `Open in Terminal` atau `Open Command Prompt here`.

### 3. Install Semua Library yang Dibutuhkan
- Ketik perintah berikut di Command Prompt:
  ```bash
  pip install opencv-python numpy matplotlib pillow
  ```
- Tunggu hingga semua proses selesai tanpa error.

---

## 1. Thermal Image-U

### Apa itu Thermal Image-U?
Aplikasi ini digunakan untuk mendeteksi dan menandai area panas pada gambar thermal tubuh manusia. Misalnya, Kamu punya foto hasil kamera thermal, aplikasi ini akan menandai bagian tubuh yang suhunya tinggi.

### Cara Menggunakan
1. Pastikan Kamu sudah punya gambar thermal (misal: download.jpeg) di folder yang sama dengan thermal.py.
2. Buka Command Prompt di folder ini.
3. Ketik:
   ```bash
   python thermal.py
   ```
4. Ikuti instruksi di layar. Biasanya Kamu akan diminta memilih file gambar.
5. Setelah diproses, akan muncul jendela baru yang menampilkan gambar asli dan hasil deteksi area panas beserta suhu area panasnya.

---
`OUTPUT :`

![Output 1](/src/Out1.png)

---

## 2. Thermal WebCam

### Apa itu Thermal WebCam?
Aplikasi ini mirip dengan thermal.py, tapi sumbernya dari webcam secara langsung (real-time). Jadi, Kamu juga bisa melihat area panas di tubuh Kamu secara langsung lewat kamera laptop/PC.

### Cara Menggunakan
1. Pastikan webcam laptop/PC Kamu aktif dan tidak sedang dipakai aplikasi lain.
2. Buka Command Prompt di folder ini.
3. Ketik:
   ```bash
   python thermalive.py
   ```
4. Akan muncul Webcam. Area panas pada tubuh Kamu akan otomatis disorot/ditandai secara real-time.
5. Untuk keluar, cukup tutup jendela video atau tekan tombol yang tersedia.

---
`OUTPUT :`

![Output 2](/src/Out2.png)
---

## 3. Thermal App

### Apa itu Thermal App?
Aplikasi ini adalah versi lebih lengkap dan mudah digunakan karena sudah berbasis tampilan (GUI/Tkinter). Anda bisa memilih: ingin analisis gambar thermal (seperti thermal.py) atau ingin analisis area panas dari webcam (seperti thermalive.py), semua lewat satu aplikasi dengan tampilan yang mudah dipahami.

### Cara Menggunakan
1. Buka Command Prompt di folder ini.
2. Ketik:
   ```bash
   python thermalapp.py
   ```
3. Akan muncul jendela aplikasi dengan dua pilihan:
   - **Analisis Gambar**: Untuk mendeteksi area panas dari file gambar.
   - **Webcam Realtime**: Untuk mendeteksi area panas dari kamera secara langsung.
4. Pilih salah satu sesuai kebutuhan, lalu ikuti instruksi di aplikasi (misal: pilih file gambar, atau izinkan akses webcam).
5. Hasil deteksi area panas dan suhu akan langsung tampil di aplikasi.
6. Tekan tombol Exit untuk menutup aplikasi.

---
`OUTPUT :`

![Output 3 - 1](/src/Out3-1.png)

---

![Output 3 - 2](/src/Out3-2.png)
---

## Catatan 
- Jika muncul error `library not found` atau `module not found`, ulangi langkah install library di atas.
- Selalu jalankan aplikasi dari Command Prompt, jangan klik dua kali file .py secara langsung.
- Jika menggunakan virtual environment, pastikan sudah aktif (ada tulisan (venv) di awal baris terminal).
- Untuk keluar dari aplikasi, cukup tutup jendela atau tekan tombol Exit.

---
