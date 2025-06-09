class DoubleStack :
    
    def __init__(self, size :int = 10):
        self.top1 = -1
        self.top2 = size
        self.stack = [None] * size
        self.size = size
        self.status : bool = True
    
    def push1(self, data: int):
        if self.top2 - self.top1 > 1:  
            self.top1 += 1
            self.stack[self.top1] = data
            self.status = True
            print(f"Data {data} berhasil dimasukkan ke Stack 1")
        else:
            self.status = False
            print('Stack 1 penuh! Tidak bisa push', data)

    def push2(self, data: int):
        if self.top2 - self.top1 > 1:
            self.top2 -= 1
            self.stack[self.top2] = data
            self.status = True
            print(f"Data {data} berhasil dimasukkan ke Stack 2")
        else:
            self.status = False
            print('Stack 2 penuh! Tidak bisa push', data)

    def pop1 (self):
        if self.top1 == -1:
            self.status = False
            return None
        
        a = self.stack[self.top1]
        self.top1 -= 1
        self.status = True
        return a

    def pop2(self):
        if self.top2 == self.size:
            self.status = False
            return None
        
        a = self.stack[self.top2]
        self.top2 += 1
        self.status = True
        return a

    def peek1 (self):
        if (self.top1) < 0:
            print("Stack kosong!")
        else:
            print(f"Data yang teratas stack adalah: {self.stack[self.top1]}")

    def peek2 (self):
        if (self.top2) >= self.size:
            print("Stack kosong!")
        else:
            print(f"Data yang teratas stack adalah: {self.stack[self.top2]}")
        
    def clear1(self):
        if self.top1 == -1:
            print("Stack 1 kosong!")
            self.status = False
        else:
            for i in range(self.top1 + 1):
                self.stack[i] = None
            self.top1 = -1
            self.status = True
            print("Stack 1 berhasil dikosongkan")

    def clear2(self):
        if self.top2 == self.size:
            print("Stack 2 kosong!")
            self.status = False
        else:
            for i in range(self.top2, self.size):
                self.stack[i] = None
            self.top2 = self.size
            self.status = True
            print("Stack 2 berhasil dikosongkan")

    def clearall(self):
        for i in range(self.size):
            self.stack[i] = None
        self.top1 = -1
        self.top2 = self.size
        self.status = True
        print("Semua stack berhasil dikosongkan")


    def print_all(self):
        print("\nStatus Stack:")
        print("Kiri (Stack 1) | Kanan (Stack 2)")
        print("-" * 12)
        
        visual = []
        for i in range(self.size):
            if i <= self.top1:
                visual.append(f"[{self.stack[i]}]")  
            elif i >= self.top2:
                visual.append(f"[{self.stack[i]}]")  
            else:
                visual.append("[ ]")  
        
        print(" ".join(visual))
        print("-" * 12)

if __name__ == "__main__":
    stack = DoubleStack()

    while True :
        print ("\nMenu")
        print ("1. Push 1")
        print ("2. Push 2")
        print ("3. Pop 1")
        print ("4. Pop 2")
        print ("5. Peek 1")
        print ("6. Peek 2")
        print ("7. Clear 1")
        print ("8. Clear 2")
        print ("9. Clear All")
        print ("10. Print All")
        print ("11. Keluar")
    
        pilihan = input("Pilihan 1 - 11 : ")

        if pilihan == "1":
            user = input("Masukkan Data: ")
            stack.push1(user)
            stack.print_all()     
        elif pilihan == "2":
            user = input("Masukkan Data: ")
            stack.push2(user)
            stack.print_all()
        elif pilihan == "3":
            print (stack.pop1())
        elif pilihan == "4":
            print (stack.pop2())
        elif pilihan == "5":
            stack.peek1()
        elif pilihan == "6":
            stack.peek2()
        elif pilihan == "7":
            stack.clear1()
        elif pilihan == "8":
            stack.clear2()
        elif pilihan == "9":
            stack.clearall()
        elif pilihan == "10":
            stack.print_all()
        elif pilihan == "11":
            break
        else:
            print("Pilihan tidak valid!")

