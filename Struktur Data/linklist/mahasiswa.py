class Mahasiswa:
    def __init__(self, nama, alamat, next=None, next2=None):
        self.nama = nama
        self.alamat = alamat
        self.next = next   
        self.next2 = next2

    def __str__(self):
        return f"Nama : {self.nama}, Alamat: {self.alamat}"

if __name__ == "__main__":
    mhs1 = Mahasiswa("Doraemon", "Tokyo")
    mhs2 = Mahasiswa("Naruto", "Konoha")
    mhs3 = Mahasiswa("Shincan", "Korea")

    mhs1.next = mhs2
    mhs1.next2 = mhs3

    mhs2.next = None

    mhs3.next = None

    ptr = mhs1
    while ptr:
        next_alamat = ptr.next.alamat if ptr.next else "Tidak Ada"
        next2_alamat = ptr.next2.alamat if ptr.next2 else "Tidak Ada"
        print(f"Nama : {ptr.nama}, Alamat : {ptr.alamat}, Tujuan MHS 2 {next_alamat}, Tujuan MHS 3 {next2_alamat}")
        ptr = ptr.next