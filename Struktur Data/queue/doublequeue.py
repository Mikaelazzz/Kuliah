class DoubleQueue:
    def __init__(self, size: int = 10):
        self.max_size = size  
        self.queue = [None] * size
        self.left_size = 0    
        self.right_size = 0  
        self.left_front = 0  
        self.left_rear = -1  
        self.right_front = size - 1 
        self.right_rear = size       
        self.status = True
        
    def pushkiri(self, data: int):
        if self.left_size + self.right_size >= self.max_size:
            self.status = False
            print('[ALERT] Queue penuh! Tidak bisa push', data)
            return
        
        self.left_rear += 1
        self.queue[self.left_rear] = data
        self.left_size += 1
        print(f"[INFO] Data {data} berhasil dimasukkan ke Queue Kiri")
        self.status = True

    def pushkanan(self, data: int):
        if self.left_size + self.right_size >= self.max_size:
            self.status = False
            print('[ALERT] Queue penuh! Tidak bisa push', data)
            return
        
        self.right_rear -= 1
        self.queue[self.right_rear] = data
        self.right_size += 1
        print(f"[INFO] Data {data} berhasil dimasukkan ke Queue Kanan")
        self.status = True

    def popkiri(self):
        if self.left_size == 0:
            self.status = False
            return None

        data = self.queue[self.left_front]

        for i in range(self.left_front + 1, self.left_rear + 1):
            self.queue[i - 1] = self.queue[i]

        self.queue[self.left_rear] = None 
        self.left_rear -= 1
        self.left_size -= 1
        self.status = True

        if self.left_size == 0:
            self.left_front = 0
            self.left_rear = -1

        return data

    def popkanan(self):
        if self.right_size == 0:
            self.status = False
            return None

        data = self.queue[self.right_front]

        for i in range(self.right_front - 1, self.right_rear - 1, -1):
            self.queue[i + 1] = self.queue[i]

        self.queue[self.right_rear] = None  
        self.right_rear += 1
        self.right_size -= 1
        self.status = True

        if self.right_size == 0:
            self.right_front = self.max_size - 1
            self.right_rear = self.max_size

        return data

    
    def clearkiri(self):
        for i in range(self.left_front, self.left_rear + 1):
            self.queue[i] = None
        self.left_size = 0
        self.left_front = 0
        self.left_rear = -1
        print("[INFO] Queue Kiri sudah dikosongkan!")
    
    def clearkanan(self):
        for i in range(self.right_front, self.right_rear - 1, -1):
            self.queue[i] = None
        self.right_size = 0
        self.right_front = self.max_size - 1
        self.right_rear = self.max_size
        print("[INFO] Queue Kanan sudah dikosongkan!")

    def clearall(self):
        self.queue = [None] * self.max_size
        self.left_size = 0
        self.right_size = 0
        self.left_front = 0
        self.left_rear = -1
        self.right_front = self.max_size - 1
        self.right_rear = self.max_size
        print("[INFO] Queue sudah dikosongkan!")

    def display(self):
        print("\n=== Queue Status ===")
        print(f"[INFO] Ukuran : {self.max_size}")
        print(f"[INFO] Posisi Kiri Berisi : {self.left_size}")
        print(f"[INFO] Posisi Kanan Berisi : {self.right_size}")
        
        print("\n[INFO] Posisi Kiri")
        if self.left_size == 0:
            print("None " * 5, end="")
        else:
            for i in range(self.left_front, min(self.left_front + 5, self.left_rear + 1)):
                print(self.queue[i], end=" ")
            for _ in range(5 - self.left_size):
                print("None", end=" ")
        
        print("\n\n[INFO] Posisi Kanan")
        if self.right_size == 0:
            print("None " * 5, end="")
        else:
            for i in range(self.right_front, max(self.right_front - 5, self.right_rear - 1), -1):
                print(self.queue[i], end=" ")
            for _ in range(5 - self.right_size):
                print("None", end=" ")
        
        print("\n\n[INFO] Queue Penuh")
        for i in range(self.max_size):
            print(f"[INFO] Index {i} : {self.queue[i]}")

    def cek_kosong(self):
        if self.left_size == 0 and self.right_size == 0:
            print("[INFO] Queue kosong!")
        elif self.left_size == 0:
            print("[INFO] Queue Kiri kosong!")
        elif self.right_size == 0:
            print("[INFO] Queue Kanan kosong!")
        else:
            print("[INFO] Queue tidak kosong!")

    def cek_penuh(self):
        if self.left_size + self.right_size >= self.max_size:
            print("[INFO] Queue penuh!")
        else:
            print("[INFO] Queue tidak penuh!")


if __name__ == "__main__":
    try:
        queue_size = 10
        n = DoubleQueue(queue_size)
    except ValueError as e:
        print(f"[404] : {e}")
        exit()

    while True:
        print("\n[ MENU QUEUE ]")
        print("[OPSI] 1. Enqueue Kiri")
        print("[OPSI] 2. Enqueue Kanan")
        print("[OPSI] 3. Dequeue Kiri")
        print("[OPSI] 4. Dequeue Kanan")
        print("[OPSI] 5. Clear Kiri")
        print("[OPSI] 6. Clear Kanan")
        print("[OPSI] 7. Clear All")
        print("[OPSI] 8. Display")
        print("[OPSI] 9. Exit")

        try:
            pilihan = int(input("[INPUT] Kamu mau pilih yang mana ? "))
            if pilihan == 1:
                data = int(input("[INPUT] Masukkan Nilai : "))
                n.pushkiri(data)
                n.display()
            elif pilihan == 2:
                data = int(input("[INPUT] Masukkan Nilai : "))
                n.pushkanan(data)
                n.display()
            elif pilihan == 3:
                popped = n.popkiri()
                if popped is not None:
                    print(f"[INFO] Data {popped} berhasil di hapus dari Queue Kiri")
                else:
                    print("[INFO] Queue Kiri kosong, tidak dapat di hapus")
                n.display()
            elif pilihan == 4:
                popped = n.popkanan()
                if popped is not None:
                    print(f"[INFO] Data {popped} berhasil di hapus dari Queue Kanan")
                else:
                    print("[INFO] Queue Kanan kosong, tidak dapat di hapus")
                n.display()
            elif pilihan == 5:
                n.clearkiri()
                n.display()
            elif pilihan == 6:
                n.clearkanan()
                n.display()
            elif pilihan == 7:
                n.clearall()
                n.display()
            elif pilihan == 8:
                n.display()
            elif pilihan == 9:
                print("[INFO] Semoga harimu menyenangkan ^.^")
                break
            else:
                print("[ALERT] Pilihan tidak valid!")
        except ValueError:
            print("[ALERT] Input tidak valid! Silakan masukkan angka.")