# Praktikum Struktur Data 
<p> Vincentius Johanes Lwie Jaya / 233408010 </p>

## Double Queue 
- Full Code : 
```python
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
```

- Output :
```
[ MENU QUEUE ]
[OPSI] 1. Enqueue Kiri
[OPSI] 2. Enqueue Kanan
[OPSI] 3. Dequeue Kiri
[OPSI] 4. Dequeue Kanan
[OPSI] 5. Clear Kiri
[OPSI] 6. Clear Kanan
[OPSI] 7. Clear All
[OPSI] 8. Display
[OPSI] 9. Exit

[INPUT] Kamu mau pilih yang mana ?
```
- Enqueue Kiri
```
[INPUT] Kamu mau pilih yang mana ? 1
[INPUT] Masukkan Nilai : 29
[INFO] Data 29 berhasil dimasukkan ke Queue Kiri

=== Queue Status ===
[INFO] Ukuran : 10
[INFO] Posisi Kiri Berisi : 1
[INFO] Posisi Kanan Berisi : 0

[INFO] Posisi Kiri
29 None None None None 

[INFO] Posisi Kanan
None None None None None 

[INFO] Index 0 : 29
[INFO] Index 1 : None
[INFO] Index 2 : None
[INFO] Index 3 : None
[INFO] Index 4 : None
[INFO] Index 5 : None
[INFO] Index 6 : None
[INFO] Index 7 : None
[INFO] Index 8 : None
[INFO] Index 9 : None
```
- Enqueue Kanan 
```
[INPUT] Kamu mau pilih yang mana ? 2
[INPUT] Masukkan Nilai : 22
[INFO] Data 22 berhasil dimasukkan ke Queue Kanan

=== Queue Status ===
[INFO] Ukuran : 10
[INFO] Posisi Kiri Berisi : 1
[INFO] Posisi Kanan Berisi : 1

[INFO] Posisi Kiri
29 None None None None

[INFO] Posisi Kanan
22 None None None None

[INFO] Index 0 : 29
[INFO] Index 1 : None
[INFO] Index 2 : None
[INFO] Index 3 : None
[INFO] Index 4 : None
[INFO] Index 5 : None
[INFO] Index 6 : None
[INFO] Index 7 : None
[INFO] Index 8 : None
[INFO] Index 9 : 22
```
- Queue Penuh
```
[INPUT] Kamu mau pilih yang mana ? 2
[INPUT] Masukkan Nilai : 55
[ALERT] Queue penuh! Tidak bisa push 55

=== Queue Status ===
[INFO] Ukuran : 10
[INFO] Posisi Kiri Berisi : 5
[INFO] Posisi Kanan Berisi : 5

[INFO] Posisi Kiri
29 21 59 24 65

[INFO] Posisi Kanan
22 32 35 88 69

[INFO] Queue Penuh

[INFO] Index 0 : 29
[INFO] Index 1 : 21
[INFO] Index 2 : 59
[INFO] Index 3 : 24
[INFO] Index 4 : 65
[INFO] Index 5 : 69
[INFO] Index 6 : 88
[INFO] Index 7 : 35
[INFO] Index 8 : 32
[INFO] Index 9 : 22
```
- Dequeue Kiri
```
[INPUT] Kamu mau pilih yang mana ? 3
[INFO] Data 29 berhasil di hapus dari Queue Kiri

=== Queue Status ===
[INFO] Ukuran : 10
[INFO] Posisi Kiri Berisi : 4
[INFO] Posisi Kanan Berisi : 5

[INFO] Posisi Kiri
21 59 24 65 None

[INFO] Posisi Kanan
22 32 35 88 69

[INFO] Index 0 : 21
[INFO] Index 1 : 59
[INFO] Index 2 : 24
[INFO] Index 3 : 65
[INFO] Index 4 : None
[INFO] Index 5 : 69
[INFO] Index 6 : 88
[INFO] Index 7 : 35
[INFO] Index 8 : 32
[INFO] Index 9 : 22
```
- Dequeue Kanan 
```
[INPUT] Kamu mau pilih yang mana ? 4
[INFO] Data 22 berhasil di hapus dari Queue Kanan

=== Queue Status ===
[INFO] Ukuran : 10
[INFO] Posisi Kiri Berisi : 4
[INFO] Posisi Kanan Berisi : 4

[INFO] Posisi Kiri
21 59 24 65 None

[INFO] Posisi Kanan
32 35 88 69 None

[INFO] Index 0 : 21
[INFO] Index 1 : 59
[INFO] Index 2 : 24
[INFO] Index 3 : 65
[INFO] Index 4 : None
[INFO] Index 5 : None
[INFO] Index 6 : 69
[INFO] Index 7 : 88
[INFO] Index 8 : 35
[INFO] Index 9 : 32
```
- Clear Kiri
```
[INPUT] Kamu mau pilih yang mana ? 5
[INFO] Queue Kiri sudah dikosongkan!

=== Queue Status ===
[INFO] Ukuran : 10
[INFO] Posisi Kiri Berisi : 0
[INFO] Posisi Kanan Berisi : 4

[INFO] Posisi Kiri
None None None None None

[INFO] Posisi Kanan
32 35 88 69 None

[INFO] Index 0 : None
[INFO] Index 1 : None
[INFO] Index 2 : None
[INFO] Index 3 : None
[INFO] Index 4 : None
[INFO] Index 5 : None
[INFO] Index 6 : 69
[INFO] Index 7 : 88
[INFO] Index 8 : 35
[INFO] Index 9 : 32
```
- Clear Kanan
```
[INPUT] Kamu mau pilih yang mana ? 6
[INFO] Queue Kanan sudah dikosongkan!

=== Queue Status ===
[INFO] Ukuran : 10
[INFO] Posisi Kiri Berisi : 0
[INFO] Posisi Kanan Berisi : 0

[INFO] Posisi Kiri
None None None None None

[INFO] Posisi Kanan
None None None None None

[INFO] Index 0 : None
[INFO] Index 1 : None
[INFO] Index 2 : None
[INFO] Index 3 : None
[INFO] Index 4 : None
[INFO] Index 5 : None
[INFO] Index 6 : None
[INFO] Index 7 : None
[INFO] Index 8 : None
[INFO] Index 9 : None
```

## Circular Queue 
- Full Code :
```python
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
                print("[INFO] Semoga harimu menyenangkan ^.^")
                break
            else:
                print("[ALERT] Pilihan tidak valid, silakan coba lagi.")
        except ValueError:
            print("[ALERT] Input harus berupa angka!")
```
- Output
```
[INFO] Size : 5 
[INFO] Mulai dari Index : 2

[ MENU CIRCULAR QUEUE ]
[OPSI] 1. Enqueue
[OPSI] 2. Dequeue
[OPSI] 3. Clear
[OPSI] 4. Display
[OPSI] 5. Exit
[INFO] Kamu mau pilih yang mana ?
```

- Enqueue 1
```
[INFO] Kamu mau pilih yang mana ? 1

[INPUT] Masukkan data: 29
[INFO] Data 29 masuk ke queue pada index 2

=== Queue Status ===
[INFO] Ukuran Queue : 5
[INFO] Mulai dari Index : 2
[INFO] Front : 2
[INFO] Rear : 2

[INFO] : None, None, 29, None, None
========================================
[INFO] Isi Queue (front ke rear): [OPSI] 29 (index:2) 

[INFO] Penyimpanan Array:
[INFO] Index 0: None
[INFO] Index 1: None
[INFO] Index 2: 29 [AWAL] [POS SEKARANG]
[INFO] Index 3: None
[INFO] Index 4: None
```
- Enqueue 2
```
[INFO] Kamu mau pilih yang mana ? 1

[INPUT] Masukkan data: 69
[INFO] Data 69 masuk ke queue pada index 3

=== Queue Status ===
[INFO] Ukuran Queue : 5
[INFO] Mulai dari Index : 2
[INFO] Front : 2
[INFO] Rear : 3

[INFO] : None, None, 29, 69, None
========================================
[INFO] Isi Queue (front ke rear): [OPSI] 29 (index:2) [OPSI] 69 (index:3)

[INFO] Penyimpanan Array:
[INFO] Index 0: None
[INFO] Index 1: None
[INFO] Index 2: 29 [AWAL]
[INFO] Index 3: 69 [POS SEKARANG]
[INFO] Index 4: None
```
- Queue Penuh
```
[INFO] Kamu mau pilih yang mana ? 1

[INPUT] Masukkan data: 66
[ALERT] Queue Penuh

=== Queue Status ===
[INFO] Ukuran Queue : 5
[INFO] Mulai dari Index : 2
[INFO] Front : 2
[INFO] Rear : 1

[INFO] : 23, 55, 29, 69, 22
========================================
[INFO] Isi Queue (front ke rear): [OPSI] 29 (index:2) [OPSI] 69 (index:3) [OPSI] 22 (index:4) [OPSI] 23 (index:0) [OPSI] 55 (index:1)

[INFO] Penyimpanan Array:
[INFO] Index 0: 23
[INFO] Index 1: 55 [POS SEKARANG]
[INFO] Index 2: 29 [AWAL]
[INFO] Index 3: 69
[INFO] Index 4: 22
```
- Dequeue
```
[INFO] Kamu mau pilih yang mana ? 2
[INFO] 29 telah dihapus dari index 2

=== Queue Status ===
[INFO] Ukuran Queue : 5
[INFO] Mulai dari Index : 2
[INFO] Front : 2
[INFO] Rear : 0

[INFO] : 55, None, 69, 22, 23
========================================
[INFO] Isi Queue (front ke rear): [OPSI] 69 (index:2) [OPSI] 22 (index:3) [OPSI] 23 (index:4) [OPSI] 55 (index:0)

[INFO] Penyimpanan Array:
[INFO] Index 0: 55 [POS SEKARANG]
[INFO] Index 1: None
[INFO] Index 2: 69 [AWAL]
[INFO] Index 3: 22
[INFO] Index 4: 23
```
- Clear
```
[INFO] Kamu mau pilih yang mana ? 3
[INFO] Queue telah clear, start index tetap 2

=== Queue Status ===
[INFO] Ukuran Queue : 5
[INFO] Mulai dari Index : 2
[INFO] Front : Empty
[INFO] Rear : Empty

[INFO] : None, None, None, None, None
========================================
[INFO] Queue kosong
```
- Enqueue Setelah Clear
```
[INFO] Kamu mau pilih yang mana ? 1

[INPUT] Masukkan data: 33
[INFO] Data 33 masuk ke queue pada index 2

=== Queue Status ===
[INFO] Ukuran Queue : 5
[INFO] Mulai dari Index : 2
[INFO] Front : 2
[INFO] Rear : 2

[INFO] : None, None, 33, None, None
========================================
[INFO] Isi Queue (front ke rear): [OPSI] 33 (index:2)

[INFO] Penyimpanan Array:
[INFO] Index 0: None
[INFO] Index 1: None
[INFO] Index 2: 33 [AWAL] [POS SEKARANG]
[INFO] Index 3: None
[INFO] Index 4: None
```
