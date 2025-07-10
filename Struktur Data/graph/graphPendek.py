class ShortestPath:
    def __init__(self):
        self.edges = []
    
    def tambah_edge(self, x, y, bobot):
        self.edges.append((x, y, bobot))
    
    def input_edges(self):
        print("[ INFO ] Masukkan edges untuk graf")
        jumlah_edge = int(input("[ INPUT ] Jumlah edge : "))
        
        for i in range(jumlah_edge):
            print(f"[ INFO ]Edge ke-{i+1}:")
            x = input("[ INPUT ] X : ")
            y = input("[ INPUT ] Y : ")
            bobot = int(input("[ INPUT ] Bobot : "))
            self.tambah_edge(x, y, bobot)
    
    def cari_jalur(self, start, target):
        jalur = []
        current = start
        bobot_total = 0
        visited = set()
        
        while current != target:
            if current in visited:
                break
            visited.add(current)
            
            found = False
            for edge in self.edges:
                if edge[0] == current:
                    jalur.append(edge)
                    bobot_total += edge[2]
                    current = edge[1]
                    found = True
                    break
            
            if not found:
                break
        
        return jalur, bobot_total
    
    def cari_semua_jalur(self, start, target, current_path=None, all_paths=None):
        if current_path is None:
            current_path = []
        if all_paths is None:
            all_paths = []
        
        if start == target:
            all_paths.append(current_path[:])
            return all_paths
        
        for edge in self.edges:
            if edge[0] == start and edge not in current_path:
                current_path.append(edge)
                self.cari_semua_jalur(edge[1], target, current_path, all_paths)
                current_path.pop()
        
        return all_paths
    
    def hitung_bobot_jalur(self, jalur):
        return sum(edge[2] for edge in jalur)
    
    def cari_jarak_terpendek(self, start, target):
        print(f"\n[ INFO ] MENCARI JARAK TERPENDEK DARI {start} KE {target}")
        
        semua_jalur = self.cari_semua_jalur(start, target)
        
        if not semua_jalur:
            print(f"[ INFO ] Tidak ada jalur dari {start} ke {target}")
            return None
        
        jalur_terpendek = None
        bobot_terpendek = float('inf')
        
        print("\n[ INFO ] Semua jalur yang ditemukan\n")
        for i, jalur in enumerate(semua_jalur):
            bobot = self.hitung_bobot_jalur(jalur)
            jalur_str = " → ".join([jalur[0][0]] + [edge[1] for edge in jalur])
            print(f"[ INFO ] Pola {chr(65+i)}: {jalur_str}")
            print(f"[ INFO ] Edges: {jalur}")
            print(f"[ INFO ] Total bobot: {bobot}\n")
            
            if bobot < bobot_terpendek:
                bobot_terpendek = bobot
                jalur_terpendek = jalur
        
        print(f"\n[ INFO ] Hasil Pencarian")
        jalur_str = " → ".join([jalur_terpendek[0][0]] + [edge[1] for edge in jalur_terpendek])
        print(f"[ INFO ] Jarak terpendek: {jalur_str}")
        print(f"[ INFO ] Total bobot: {bobot_terpendek}")
        
        return jalur_terpendek, bobot_terpendek
    
    def tampilkan_graf(self):
        print("\n[ INFO ] Edge yang ada dalam Graf")
        for edge in self.edges:
            print(f"[ INFO ] Edge dari {edge[0]} ke {edge[1]} dengan bobot {edge[2]}")

def main():
    graf = ShortestPath()
    
    graf.input_edges()
    
    graf.tampilkan_graf()
    
    print("\n[ INFO ] Node Asal dan Tujuan")
    start = input("[ INPUT ] MULAI : ")
    target = input("[ INPUT ] TUJUAN : ")
    
    graf.cari_jarak_terpendek(start, target)

if __name__ == "__main__":
    main()