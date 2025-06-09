class SortedQueue :
    def __init__(self, size: int = 10):
        self.size = size
        self.stack = [None] * size
        self.panjang = 0

    def kosong (self):
        return self.panjang == 0
    
    def penuh (self):
        return self.panjang == self.size
    
    def __init__(self, size: int = 10):
        self.size = size
        self.stack = [None] * size
        self.panjang = 0

    def kosong(self):
        return self.panjang == 0
    
    def penuh(self):
        return self.panjang == self.size
    
    def enqueue(self, item):
        if self.penuh():
            print("[ALERT] Queue Penuh")
            return False
        else:
            try:
                item = int(item)
            except:
                pass
                
            self.stack[self.panjang] = item
            self.panjang += 1

            for i in range(self.panjang):
                for j in range(0, self.panjang - i - 1):
                    if type(self.stack[j]) == type(self.stack[j+1]):
                        if self.stack[j] > self.stack[j+1]:
                            self.stack[j], self.stack[j+1] = self.stack[j+1], self.stack[j]
                    elif type(self.stack[j+1]) == int and type(self.stack[j]) == str:
                        self.stack[j], self.stack[j+1] = self.stack[j+1], self.stack[j]

            print(f"[INFO] Data {item} masuk ke Queue")
            return True


    def dequeue(self):
        if self.kosong():
            print("[ALERT] Queue Kosong")
            return None
        
        item = self.stack[0]
        for i in range(1, self.panjang):
            self.stack[i - 1] = self.stack[i]
        self.stack[self.panjang - 1] = None
        self.panjang -= 1
        
        print(f"[INFO] {item} telah dihapus")
        return item
    
    def clear(self):
        self.stack = [None] * self.size
        self.panjang = 0
        print("[INFO] Queue telah clear")

    def display(self):
        print("[INFO] Isi Queue :", end=" ")
        for i in range(self.size):
            if self.stack[i] is not None:
                print(self.stack[i], end=" ")
            else:
                print("None", end=" ")
        print()  

if __name__ == "__main__":
    queue = 5
    n = SortedQueue(queue)
    
    while True :
        print("\n[ MENU QUEUE ]")
        print("1. Enqueue")
        print("2. Dequeue")
        print("3. Clear")
        print("4. Display")
        print("5. Exit")
        
        choice = int(input("[INFO] Pilih menu: "))
        
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
            print("[INFO] Keluar dari program")
            break
        else:
            print("[ALERT] Pilihan tidak valid, silakan coba lagi.")
