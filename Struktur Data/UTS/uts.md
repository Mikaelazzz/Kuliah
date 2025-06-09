<p align="center" style="font-size:40px; font-weight:bold" >
UTS
</p>

<p align="center" >
Vincentius Johanes Lwie Jaya 233408010
</p>

`FULL CODE :`

```python
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

```

`OUTPUT :`

```
[ MENU QUEUE ]
1. Enqueue
2. Dequeue
3. Clear
4. Display
5. Exit
[INFO] Pilih menu:
```

`INPUT KE 1`

``` 
[INFO] Pilih menu: 1

[INPUT] Masukkan data: 20
[INFO] Data 20 masuk ke Queue
[INFO] Isi Queue : 20 None None None None 
```

`INPUT KE 2`

```
[INFO] Pilih menu: 1

[INPUT] Masukkan data: 10
[INFO] Data 10 masuk ke Queue
[INFO] Isi Queue : 10 20 None None None
```

`INPUT KE 3`

```
[INFO] Pilih menu: 1

[INPUT] Masukkan data: 40
[INFO] Data 40 masuk ke Queue
[INFO] Isi Queue : 10 20 40 None None
```

`INPUT KE 4`

```
[INFO] Pilih menu: 1

[INPUT] Masukkan data: 30
[INFO] Data 30 masuk ke Queue
[INFO] Isi Queue : 10 20 30 40 None
```

`INPUT KE 5`

```
[INFO] Pilih menu: 1

[INPUT] Masukkan data: 5
[INFO] Data 5 masuk ke Queue
[INFO] Isi Queue : 5 10 20 30 40
```

`INPUT KE 6 [QUEUE PENUH]`
```
[INFO] Pilih menu: 1

[INPUT] Masukkan data: 23
[ALERT] Queue Penuh
[INFO] Isi Queue : 5 10 20 30 40
```

`HAPUS KE 1`
```
[INFO] Pilih menu: 2
[INFO] 5 telah dihapus
[INFO] Isi Queue : 10 20 30 40 None
```

`HAPUS KE 2`
```
[INFO] Pilih menu: 2
[INFO] 10 telah dihapus
[INFO] Isi Queue : 20 30 40 None None
```

`HAPUS KE 3`
```
[INFO] Pilih menu: 2
[INFO] 20 telah dihapus
[INFO] Isi Queue : 30 40 None None None
```

`HAPUS KE 4`
```
[INFO] Pilih menu: 2
[INFO] 30 telah dihapus
[INFO] Isi Queue : 40 None None None None
```

`HAPUS KE 5`
```
[INFO] Pilih menu: 2
[INFO] 40 telah dihapus
[INFO] Isi Queue : None None None None None
```

`HAPUS KE 6`
```
[INFO] Pilih menu: 2
[ALERT] Queue Kosong
[INFO] Isi Queue : None None None None None
```

`FULL DATA SEBELUM CLEAR`
```
[INFO] Pilih menu: 4
[INFO] Isi Queue : 5 10 20 30 40
```

`SETELAH CLEAR`
```
[INFO] Pilih menu: 3
[INFO] Queue telah clear
[INFO] Isi Queue : None None None None None
```