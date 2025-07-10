import random

class PlantNode:
    def __init__(self, name, growth_rate):
        self.name = name # Nama cabang/daun
        self.children = [] # Daftar cabang/daun
        self.growth_rate = growth_rate # Tingkat pertumbuhan (0-1)
    
    # Pertumbuhan otomatis cabang/daun
    # Jika growth_rate > 0.5, cabang akan tumbuh lebih cepat
    def grow(self):
        if random.random() < self.growth_rate and len(self.children) < 3:
            # Pastikan nama cabang unik di parent
            new_name = f"{self.name}.{len(self.children)+1}" 
            self.children.append(PlantNode(new_name, max(0.1, self.growth_rate - 0.1)))
        for child in self.children:
            child.grow()
    
    # Cetak struktur pohon tanaman
    def print_tree(self, level=0):
        print("  " * level + f"{self.name} (rate: {self.growth_rate:.2f})")
        for child in self.children:
            child.print_tree(level + 1)
    
    # Cari cabang/daun berdasarkan nama
    # Mengembalikan node jika ditemukan, atau None jika tidak ada
    def find(self, name):
        if self.name == name:
            return self
        for child in self.children:
            found = child.find(name)
            if found:
                return found
        return None
    
    # Cek apakah nama cabang/daun sudah ada di pohon
    # Mengembalikan True jika ada, False jika tidak
    def exists(self, name):
        if self.name == name:
            return True
        return any(child.exists(name) for child in self.children)
    
    # Hapus cabang/daun berdasarkan nama
    # Mengembalikan True jika berhasil dihapus, False jika tidak ditemukan
    def remove_child(self, name):
        for i, child in enumerate(self.children):
            if child.name == name:
                del self.children[i]
                return True
            if child.remove_child(name):
                return True
        return False

# Menu interaktif
if __name__ == "__main__":
    root = PlantNode("Bibit A", 0.8)
    while True:
        print("\nMenu:")
        print("1. Tambah cabang/daun secara manual")
        print("2. Simulasi pertumbuhan otomatis (1 hari)")
        print("3. Lihat struktur tanaman")
        print("4. Hapus cabang/daun tertentu")
        print("5. Keluar")
        pilihan = input("Pilih menu [1-5]: ")
        if pilihan == '1':
            parent_name = input("Masukkan nama parent (misal: Tanaman A): ")
            parent = root.find(parent_name)
            if parent:
                cabang_name = input("Masukkan nama cabang/daun baru: ")
                if root.exists(cabang_name):
                    print(f"Nama '{cabang_name}' sudah ada di pohon. Pilih nama lain.")
                    continue
                rate = input("Masukkan growth rate (0-1, default 0.5): ")
                try:
                    rate = float(rate)
                    if not (0 <= rate <= 1):
                        print("Growth rate harus antara 0 dan 1. Menggunakan default 0.5.")
                        rate = 0.5
                except ValueError:
                    rate = 0.5
                parent.children.append(PlantNode(cabang_name, rate))
                print(f"Cabang '{cabang_name}' berhasil ditambahkan ke '{parent_name}'.")
            else:
                print("Parent tidak ditemukan.")
        elif pilihan == '2':
            before = sum(1 for _ in root.children)
            root.grow()
            after = sum(1 for _ in root.children)
            print(f"Simulasi pertumbuhan 1 hari selesai. Jumlah cabang utama: {len(root.children)}")
        elif pilihan == '3':
            print("Struktur tanaman:")
            root.print_tree()
        elif pilihan == '4':
            del_name = input("Masukkan nama cabang/daun yang ingin dihapus: ")
            if del_name == root.name:
                print("Tidak bisa menghapus akar tanaman.")
            elif root.remove_child(del_name):
                print(f"Cabang '{del_name}' berhasil dihapus.")
            else:
                print("Cabang tidak ditemukan.")
        elif pilihan == '5':
            print("Terima kasih telah menggunakan simulasi tanaman!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")