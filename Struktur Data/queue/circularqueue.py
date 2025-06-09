import random

class CircularQueue:
    def __init__(self, size: int = 10, mulai: int = 0):        
        self.size = size
        self.queue = [None] * size
        self.front = -1  
        self.rear = -1  
        self.mulai = mulai
        
    def is_empty(self):
        return self.front == -1
    
    def is_full(self):
        return (self.rear + 1) % self.size == self.front
    
    def enqueue(self, item):
        if self.is_full():
            print("[ALERT] Queue Penuh")
            return False
        
        if self.is_empty():
            self.front = self.mulai
            self.rear = self.mulai
        else:
            self.rear = (self.rear + 1) % self.size
            
        self.queue[self.rear] = item
        print(f"[INFO] Data {item} masuk ke queue pada index {self.rear}")
        return True
    
    def dequeue(self):
        if self.is_empty():
            print("[ALERT] Queue Kosong")
            return None
        
        item = self.queue[self.front]
        self.queue[self.front] = None  
        
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            current = self.front
            next_pos = (current + 1) % self.size
            while current != self.rear:
                self.queue[current] = self.queue[next_pos]
                current = next_pos
                next_pos = (next_pos + 1) % self.size
            self.queue[self.rear] = None
            self.rear = (self.rear - 1) % self.size
            
        print(f"[INFO] {item} telah dihapus dari index {self.front}")
        return item
    
    def clear(self):
        self.queue = [None] * self.size
        self.front = -1
        self.rear = -1
        print(f"[INFO] Queue telah clear, start index tetap {self.mulai}")

    def display(self):
        print("\n=== Queue Status ===")
        print(f"[INFO] Ukuran Queue : {self.size}")
        print(f"[INFO] Mulai dari Index : {self.mulai}")
        print(f"[INFO] Front : {self.front if self.front != -1 else 'Empty'}")
        print(f"[INFO] Rear : {self.rear if self.rear != -1 else 'Empty'}")
        

        # Tampilkan isi array dalam format yang diminta
        print("\n[INFO] : ", end="")
        print(", ".join(str(item) if item is not None else "None" for item in self.queue))

        print("=" * 40)
            
        if self.is_empty():
            print("[INFO] Queue kosong")
            return
            
        print("[INFO] Isi Queue (front ke rear):", end=" ")
        i = self.front
        count = 0
        while True:
            print(f"[OPSI] {self.queue[i]} (index:{i})", end=" ")
            count += 1
            if i == self.rear:
                break
            i = (i + 1) % self.size
            
            if count > self.size:
                print("\n[ALERT] Terjadi kesalahan struktur queue!")
                break
        print()
        
        print("\n[INFO] Penyimpanan Array:")
        for idx, val in enumerate(self.queue):
            marker = ""
            if idx == self.front:
                marker += " [AWAL]"
            if idx == self.rear:
                marker += " [POS SEKARANG]"
            print(f"[INFO] Index {idx}: {val}{marker}")

if __name__ == "__main__":
    try:
        size = 5
        mulai = random.randint(0, size - 1)
            
        n = CircularQueue(size, mulai)
        print(f"[INFO] Size : {size} \n[INFO] Mulai dari Index : {mulai}")
    except ValueError as e:
        print(f"[ALERT] {e}")
        exit()

    while True:
        print("\n[ MENU CIRCULAR QUEUE ]")
        print("[OPSI] 1. Enqueue")
        print("[OPSI] 2. Dequeue")
        print("[OPSI] 3. Clear")
        print("[OPSI] 4. Display")
        print("[OPSI] 5. Exit")
        
        try:
            choice = int(input("[INFO] Kamu mau pilih yang mana ? "))
            
            if choice == 1:
                item = input("\n[INPUT] Masukkan data: ")
                n.enqueue(item)
                n.display()
            elif choice == 2:
                n.dequeue()
                n.display()
            elif choice == 3:
                n.clear()
                n.display()
            elif choice == 4:
                n.display()
            elif choice == 5:
                print("[INFO] Semoga harimu menyenangkan ^.^")
                break
            else:
                print("[ALERT] Pilihan tidak valid, silakan coba lagi.")
        except ValueError:
            print("[ALERT] Input harus berupa angka!")
