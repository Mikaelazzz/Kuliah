import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import math

class ShortestPath:
    def __init__(self):
        self.edges = []
    
    def tambah_edge(self, x, y, bobot):
        """Menambahkan edge ke dalam graf"""
        self.edges.append((x, y, bobot))
    
    def input_edges(self):
        """Input edges dari pengguna"""
        print("=== INPUT EDGES ===")
        jumlah_edge = int(input("Masukkan jumlah edge: "))
        
        for i in range(jumlah_edge):
            print(f"Edge ke-{i+1}:")
            x = input("Node asal: ")
            y = input("Node tujuan: ")
            bobot = int(input("Bobot: "))
            self.tambah_edge(x, y, bobot)
    
    def cari_jalur(self, start, target):
        """Mencari jalur dari start ke target"""
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
        """Mencari semua jalur yang mungkin dari start ke target"""
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
        """Menghitung total bobot dari sebuah jalur"""
        return sum(edge[2] for edge in jalur)
    
    def cari_jarak_terpendek(self, start, target):
        """Mencari jarak terpendek dari start ke target"""
        print(f"\n=== MENCARI JARAK TERPENDEK DARI {start} KE {target} ===")
        
        # Cari semua jalur yang mungkin
        semua_jalur = self.cari_semua_jalur(start, target)
        
        if not semua_jalur:
            print(f"Tidak ada jalur dari {start} ke {target}")
            return None, None, None
        
        jalur_terpendek = None
        bobot_terpendek = float('inf')
        
        print("\nSemua jalur yang ditemukan:")
        for i, jalur in enumerate(semua_jalur):
            bobot = self.hitung_bobot_jalur(jalur)
            jalur_str = " → ".join([jalur[0][0]] + [edge[1] for edge in jalur])
            print(f"Pola {chr(65+i)}: {jalur_str}")
            print(f"  Edges: {jalur}")
            print(f"  Total bobot: {bobot}")
            
            if bobot < bobot_terpendek:
                bobot_terpendek = bobot
                jalur_terpendek = jalur
        
        print(f"\n=== HASIL ===")
        jalur_str = " → ".join([jalur_terpendek[0][0]] + [edge[1] for edge in jalur_terpendek])
        print(f"Jarak terpendek: {jalur_str}")
        print(f"Total bobot: {bobot_terpendek}")
        
        return jalur_terpendek, bobot_terpendek, semua_jalur
    
    def tampilkan_graf(self):
        """Menampilkan semua edges dalam graf"""
        print("\n=== GRAF YANG DIBUAT ===")
        for edge in self.edges:
            print(f"Edge dari {edge[0]} ke {edge[1]} dengan bobot {edge[2]}")
    
    def get_all_nodes(self):
        """Mendapatkan semua node yang ada dalam graf"""
        nodes = set()
        for edge in self.edges:
            nodes.add(edge[0])
            nodes.add(edge[1])
        return list(nodes)

class GraphVisualizer:
    def __init__(self, graph):
        self.graph = graph
        self.root = tk.Tk()
        self.root.title("Graph Shortest Path Visualizer")
        self.root.geometry("1200x800")
        
        # Frame utama dengan 3 kolom
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame kiri untuk input
        left_frame = tk.Frame(main_frame, width=300, relief=tk.RIDGE, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Frame kanan untuk canvas dan hasil
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # === SETUP INPUT FRAME ===
        tk.Label(left_frame, text="INPUT EDGES", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        
        # Input untuk node asal
        tk.Label(left_frame, text="Node Asal:").pack(anchor=tk.W, padx=10)
        self.entry_asal = tk.Entry(left_frame, width=20)
        self.entry_asal.pack(padx=10, pady=(0, 5))
        
        # Input untuk node tujuan
        tk.Label(left_frame, text="Node Tujuan:").pack(anchor=tk.W, padx=10)
        self.entry_tujuan = tk.Entry(left_frame, width=20)
        self.entry_tujuan.pack(padx=10, pady=(0, 5))
        
        # Input untuk bobot
        tk.Label(left_frame, text="Bobot:").pack(anchor=tk.W, padx=10)
        self.entry_bobot = tk.Entry(left_frame, width=20)
        self.entry_bobot.pack(padx=10, pady=(0, 10))
        
        # Button untuk menambah edge
        tk.Button(left_frame, text="Tambah Edge", command=self.tambah_edge, bg="lightgreen").pack(pady=5)
        
        # Button untuk clear edges
        tk.Button(left_frame, text="Clear All Edges", command=self.clear_edges, bg="lightcoral").pack(pady=5)
        
        # Separator
        tk.Label(left_frame, text="─" * 30).pack(pady=10)
        
        # Listbox untuk menampilkan edges
        tk.Label(left_frame, text="EDGES YANG DIBUAT:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10)
        
        # Frame untuk listbox dan scrollbar
        listbox_frame = tk.Frame(left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.edges_listbox = tk.Listbox(listbox_frame, height=8)
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.edges_listbox.yview)
        self.edges_listbox.config(yscrollcommand=scrollbar.set)
        
        self.edges_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button untuk hapus edge yang dipilih
        tk.Button(left_frame, text="Hapus Edge Terpilih", command=self.hapus_edge_terpilih, bg="orange").pack(pady=5)
        
        # Separator
        tk.Label(left_frame, text="─" * 30).pack(pady=10)
        
        # Section untuk pencarian jalur terpendek
        tk.Label(left_frame, text="PENCARIAN JALUR", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        # Input untuk node asal pencarian
        tk.Label(left_frame, text="Dari Node:").pack(anchor=tk.W, padx=10)
        self.entry_start = tk.Entry(left_frame, width=20)
        self.entry_start.pack(padx=10, pady=(0, 5))
        
        # Input untuk node tujuan pencarian
        tk.Label(left_frame, text="Ke Node:").pack(anchor=tk.W, padx=10)
        self.entry_target = tk.Entry(left_frame, width=20)
        self.entry_target.pack(padx=10, pady=(0, 10))
        
        # Button untuk mencari jalur terpendek
        tk.Button(left_frame, text="Cari Jalur Terpendek", command=self.find_shortest_path, bg="lightblue").pack(pady=5)
        
        # === SETUP RIGHT FRAME ===
        # Canvas untuk menggambar graf
        self.canvas = tk.Canvas(right_frame, width=600, height=400, bg="white", relief=tk.RIDGE, bd=2)
        self.canvas.pack(pady=(0, 10))
        
        # Frame untuk control buttons
        control_frame = tk.Frame(right_frame)
        control_frame.pack(pady=5)
        
        # Button untuk menggambar graf
        tk.Button(control_frame, text="Draw Graph", command=self.draw_graph, bg="lightgreen").pack(side=tk.LEFT, padx=5)
        
        # Button untuk clear canvas
        tk.Button(control_frame, text="Clear Canvas", command=self.clear_canvas, bg="lightcoral").pack(side=tk.LEFT, padx=5)
        
        # Text area untuk menampilkan hasil
        tk.Label(right_frame, text="HASIL PENCARIAN:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        # Frame untuk text area dan scrollbar
        text_frame = tk.Frame(right_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, height=15, width=70)
        text_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=text_scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Posisi node dan jalur terpendek
        self.node_positions = {}
        self.shortest_path_edges = []
        
        # Bind Enter key untuk input
        self.entry_bobot.bind('<Return>', lambda event: self.tambah_edge())
        self.entry_target.bind('<Return>', lambda event: self.find_shortest_path())
    
    def tambah_edge(self):
        """Menambah edge ke dalam graf"""
        try:
            asal = self.entry_asal.get().strip()
            tujuan = self.entry_tujuan.get().strip()
            bobot_str = self.entry_bobot.get().strip()
            
            if not asal or not tujuan or not bobot_str:
                messagebox.showwarning("Warning", "Semua field harus diisi!")
                return
            
            bobot = int(bobot_str)
            
            # Tambah edge ke graf
            self.graph.tambah_edge(asal, tujuan, bobot)
            
            # Update listbox
            self.update_edges_listbox()
            
            # Clear input fields
            self.entry_asal.delete(0, tk.END)
            self.entry_tujuan.delete(0, tk.END)
            self.entry_bobot.delete(0, tk.END)
            
            # Focus ke field pertama
            self.entry_asal.focus()
            
        except ValueError:
            messagebox.showerror("Error", "Bobot harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def update_edges_listbox(self):
        """Update listbox edges"""
        self.edges_listbox.delete(0, tk.END)
        for i, edge in enumerate(self.graph.edges):
            self.edges_listbox.insert(tk.END, f"{i+1}. {edge[0]} → {edge[1]} (bobot: {edge[2]})")
    
    def hapus_edge_terpilih(self):
        """Hapus edge yang dipilih dari listbox"""
        selection = self.edges_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Pilih edge yang ingin dihapus!")
            return
        
        index = selection[0]
        del self.graph.edges[index]
        self.update_edges_listbox()
        
        # Clear canvas jika ada
        if self.shortest_path_edges:
            self.shortest_path_edges = []
            self.draw_graph()
    
    def clear_edges(self):
        """Clear semua edges"""
        self.graph.edges = []
        self.edges_listbox.delete(0, tk.END)
        self.clear_canvas()
        self.result_text.delete(1.0, tk.END)
    
    def calculate_node_positions(self):
        """Menghitung posisi node dalam canvas"""
        nodes = self.graph.get_all_nodes()
        if not nodes:
            return
        
        center_x, center_y = 300, 200
        radius = 120
        
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[node] = (x, y)
    
    def draw_graph(self):
        """Menggambar graf pada canvas"""
        self.clear_canvas()
        
        if not self.graph.edges:
            return
        
        self.calculate_node_positions()
        
        # Gambar edges
        for edge in self.graph.edges:
            x1, y1 = self.node_positions[edge[0]]
            x2, y2 = self.node_positions[edge[1]]
            
            # Cek apakah edge ini adalah bagian dari jalur terpendek
            color = "red" if edge in self.shortest_path_edges else "black"
            width = 3 if edge in self.shortest_path_edges else 1
            
            # Gambar garis
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, arrow=tk.LAST, arrowshape=(16, 20, 6))
            
            # Hitung posisi untuk label bobot
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Gambar bobot
            self.canvas.create_text(mid_x, mid_y - 10, text=str(edge[2]), fill="blue", font=("Arial", 10, "bold"))
        
        # Gambar nodes
        for node, (x, y) in self.node_positions.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue", outline="black", width=2)
            self.canvas.create_text(x, y, text=str(node), font=("Arial", 12, "bold"))
    
    def find_shortest_path(self):
        """Mencari jalur terpendek"""
        if not self.graph.edges:
            messagebox.showwarning("Warning", "Belum ada edges yang diinput!")
            return
        
        try:
            start = self.entry_start.get().strip()
            target = self.entry_target.get().strip()
            
            if not start or not target:
                messagebox.showwarning("Warning", "Node asal dan tujuan harus diisi!")
                return
            
            # Cari jarak terpendek
            jalur_terpendek, bobot_terpendek, semua_jalur = self.graph.cari_jarak_terpendek(start, target)
            
            # Update hasil di text area
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"=== MENCARI JARAK TERPENDEK DARI {start} KE {target} ===\n\n")
            
            if jalur_terpendek is None:
                self.result_text.insert(tk.END, f"Tidak ada jalur dari {start} ke {target}\n")
                return
            
            self.result_text.insert(tk.END, "Semua jalur yang ditemukan:\n")
            for i, jalur in enumerate(semua_jalur):
                bobot = self.graph.hitung_bobot_jalur(jalur)
                jalur_str = " → ".join([jalur[0][0]] + [edge[1] for edge in jalur])
                self.result_text.insert(tk.END, f"Pola {chr(65+i)}: {jalur_str}\n")
                self.result_text.insert(tk.END, f"  Edges: {jalur}\n")
                self.result_text.insert(tk.END, f"  Total bobot: {bobot}\n\n")
            
            self.result_text.insert(tk.END, "=== HASIL ===\n")
            jalur_str = " → ".join([jalur_terpendek[0][0]] + [edge[1] for edge in jalur_terpendek])
            self.result_text.insert(tk.END, f"Jarak terpendek: {jalur_str}\n")
            self.result_text.insert(tk.END, f"Total bobot: {bobot_terpendek}\n")
            
            # Highlight jalur terpendek pada graf
            self.shortest_path_edges = jalur_terpendek
            self.draw_graph()
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def clear_canvas(self):
        """Membersihkan canvas"""
        self.canvas.delete("all")
        self.shortest_path_edges = []
    
    def run(self):
        """Menjalankan aplikasi"""
        self.root.mainloop()

def main():
    graf = ShortestPath()
    
    # Pilihan mode
    print("Pilih mode:")
    print("1. Console Mode")
    print("2. GUI Mode")
    choice = input("Pilihan (1/2): ")
    
    if choice == "1":
        # Console mode
        graf.input_edges()
        graf.tampilkan_graf()
        
        print("\n=== PENCARIAN JARAK TERPENDEK ===")
        start = input("Masukkan node asal: ")
        target = input("Masukkan node tujuan: ")
        
        graf.cari_jarak_terpendek(start, target)
    
    elif choice == "2":
        # GUI mode
        visualizer = GraphVisualizer(graf)
        visualizer.run()
    
    else:
        print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()