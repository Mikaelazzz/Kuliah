class Stack:
    def __init__(self, size :int = 5):
        self.size = size
        self.stack = []
        self.status : bool = True
        

    def push (self, user : int):
        if len(self.stack) < self.size:
            self.stack.append(user)
            print(f"{user} berhasil ditambahkan ke dalam stack")
        else:
            print("Stack penuh!")

    def pop (self):
        if len(self.stack) == 0:
            print("Stack kosong!")
        else:
            print(f"{self.stack.pop()} berhasil dihapus dari stack")

    def clear (self):
        self.stack.clear()
        print("Stack berhasil dikosongkan")

    def peek (self):
        if len(self.stack) == 0:
            print("Stack kosong!")
        else:
            print(f"Data yang teratas stack adalah: {self.stack[-1]}")


if __name__ == "__main__":
    stack = Stack()
    status = True
    
    while status == True:
        print("\nMenu:")
        print("1. Push Data")
        print("2. Pop Data")
        print("3. Clear Stack")
        print("4. Peek Data")
        print("5. Keluar")

        pilihan = input("Masukkan pilihan Anda (1-5): ")

        if pilihan == "1":
            user = input("Masukkan Data: ")
            stack.push(user)
        elif pilihan == "2":
            stack.pop()
        elif pilihan == "3":
            stack.clear()
        elif pilihan == "4":
            stack.peek()
        elif pilihan == "5":
            status = False
        else:
            print("Pilihan tidak valid!")