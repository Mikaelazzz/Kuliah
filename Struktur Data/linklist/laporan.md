# Laporan Praktikum 

Vincentius Johanes Lwie Jaya / 233408010

## FULL CODE : 

```python 
class Mahasiswa:
    def __init__(self, nama, alamat, next=None, next2=None):
        self.nama = nama # Nama Mahasiswa
        self.alamat = alamat # Alamat Mahasiswa
        self.next = next   # Tujuan Pertama
        self.next2 = next2 # Tujuan Kedua

    def __str__(self):
        # Untuk Print Nama dengan Format
        return f"Nama : {self.nama}, Alamat: {self.alamat}" 

if __name__ == "__main__":
    # Objek Mahasiswa 1-3
    mhs1 = Mahasiswa("Doraemon", "Tokyo")
    mhs2 = Mahasiswa("Naruto", "Konoha")
    mhs3 = Mahasiswa("Shincan", "Korea")

    # Membuat Mahasiswa 1 Memiliki Tujuan Alamat ke Mahasiswa 2 dan 3
    mhs1.next = mhs2
    mhs1.next2 = mhs3

    # Membuat Mahasiswa 2 tidak memiliki tujuan Alamat = None
    mhs2.next = None

    # Membuat Mahasiswa 3 tidak memiliki tujuan Alamat = None
    mhs3.next = None

    
    ptr = mhs1 # Pointer / Top
    while ptr:
        # Membuat kondisi ketika Tujuan Alamat yang di tuju adalah None akan menampilkan pesan "Tidak Ada" 
        next_alamat = ptr.next.alamat if ptr.next else "Tidak Ada" 

        # Membuat kondisi ketika Tujuan Alamat yang di tuju adalah None akan menampilkan pesan "Tidak Ada" 
        next2_alamat = ptr.next2.alamat if ptr.next2 else "Tidak Ada" 

        # Menampilkan Data 
        print(f"Nama : {ptr.nama}, Alamat : {ptr.alamat}, Tujuan MHS 2 {next_alamat}, Tujuan MHS 3 {next2_alamat}")
        ptr = ptr.next # Mengambil data dari Tujuan Alamat ke 1
```

- Output :

```
Nama : Doraemon, Alamat : Tokyo, Tujuan MHS 2 Konoha, Tujuan MHS 3 Korea
Nama : Naruto, Alamat : Konoha, Tujuan MHS 2 Tidak Ada, Tujuan MHS 3 Tidak Ada
```
