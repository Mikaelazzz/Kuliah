import random 

class CircularStack:
    def __init__(self, size: int = 10, index: int = 0):
        self.size = size
        self.stack = [None] * size
        self.posisi = -1
        self.index = index

    def kosong(self):
        return self.posisi == -1
    
    def penuh(self):
        return self.posisi == self.size - 1
    
    def push(self, item):
        if self.penuh():
            self.index = (self.index) % self.size
            print("Data telah Penuh")
            return False
        else:
            self.posisi += 1
            position = (self.index + self.posisi) % self.size
            self.stack[position] = item
            print(f"Data {item} masuk ke stack pada index {position}")
            return True

    def pop(self):
        if self.kosong():
            print("Stack Kosong")
            return None
        
        position = (self.index + self.posisi) % self.size
        item = self.stack[position]
        self.stack[position] = None
        self.posisi -= 1
        
        if self.kosong():
            self.index = 0
            
        print(f"{item} telah dihapus")
        return item
    
    def peek(self):
        if self.kosong():
            print("Stack Kosong")
            return None
        
        position = (self.index + self.posisi) % self.size
        return self.stack[position]

    def clear(self):
        self.stack = [None] * self.size
        self.posisi = -1
        self.index = 0
        print("Stack telah clear")

    def display(self):
        if self.kosong():
            print("Stack kosong")
            return
        
        print("Isi Stack saat ini:")
        for i in range(self.posisi + 1):
            position = (self.index + i) % self.size
            print(f"[{position}]: {self.stack[position]}")

if __name__ == "__main__":
    size = 5
    mulai = random.randint(0, size - 1)
    rounded = CircularStack(size, mulai)  
    
    while True:
        print("\nOperasi Circular Stack:")
        print("1. Push")
        print("2. Pop")
        print("3. Peek")
        print("4. Clear")
        print("5. Display")
        print("6. Exit")
        
        choice = input("Masukkan pilihan (1-6): ")
        
        if choice == '1':
            user = input("Masukkan item yang akan di-push: ")
            rounded.push(user)
        elif choice == '2':
            item = rounded.pop()
            if item is not None:
                print(f"Item yang di-pop: {item}")
        elif choice == '3':
            item = rounded.peek()
            if item is not None:
                print(f"Item teratas: {item}")
        elif choice == '4':
            rounded.clear()
        elif choice == '5':
            rounded.display()
        elif choice == '6':
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")