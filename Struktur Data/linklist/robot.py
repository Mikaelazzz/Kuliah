class Doraemon():
    nama = None
    kelas = None
    gender = None
    umur = None

dora1 = Doraemon()
dora2 = Doraemon()

dora1.nama = "Nobita" 
dora1.kelas = "4 SD"
dora1.gender = "Laki - Laki"
dora1.umur = 13

dora2.nama = "Shizuka" 
dora2.kelas = "4 SD"

dora2.gender = "Perempuan"
dora2.umur = 11

print (dora1.nama)
print (dora1.umur)

print("\n")

print (dora2.nama)
print (dora2.umur)

print("\n")

class Robot():
    def __init__(self, nama, jabatan, umur, gender, affinitas) -> None: 
        self.nama = nama
        self.jabatan = jabatan
        self.umur = umur
        self.gender = gender
        self.affinitas = affinitas

    # def User1 (self):
        # self.nama = "Naruto"
        # self.jabatan = "Hokage"
        # self.umur = "21"
        # self.gender = "Laki - Laki"

    # def User2 (self):
    #     self.nama = "Hinata"
    #     self.jabatan = "Jonin"
    #     self.umur = "19"
    #     self.gender = "Perempuan"


if __name__ == "__main__":
    user1 = Robot("Naruto", "Hokage", "21", "Laki", None)
    user2 = Robot("Hinata", "Jonin","19", "Perempuan", None)
    user3 = Robot("Ten Ten", "Jonin","19", "Perempuan", None)
    user4 = Robot("Sakura", "Jonin","19", "Perempuan", None)
    user5 = Robot("Haku", "Chunin","15", "Perempuan", None)
    user6 = Robot("Sasuke", "Jonin","21", "Laki", None)
    user7 = Robot("Minato", "Jonin","30", "Laki", None)
    # user1.affinitas = user2
    # user2.affinitas = user4
    # user4.affinitas = user6
    # user1.affinitas = user7
    # user1.affinitas = user6
    user1.affinitas = user2
    user2.affinitas = user3
    user3.affinitas = user4
    user4.affinitas = user6

    ptr = user1
    while ptr:
        # print(ptr.nama)
        # print(ptr.jabatan)
        # print(ptr.umur)
        # print(ptr.gender)
        print(f'{ptr.nama},{ptr.jabatan},{ptr.umur},{ptr.gender},{ptr.affinitas} ')
        ptr = ptr.affinitas
        # print("\n")
