import random

class DungeonNode:
    def __init__(self, name, room_type, encounter_chance=0.3):
        self.name = name  # Nama ruangan
        self.room_type = room_type  # Jenis ruangan (start, monster, treasure, exit, etc.)
        self.children = []  # Ruangan yang terhubung
        self.encounter_chance = encounter_chance  # Peluang bertemu musuh
        self.visited = False  # Apakah ruangan sudah dikunjungi
        self.loot = None  # Harta karun jika ada
    
    # Eksplorasi otomatis dungeon
    def explore(self, depth=0, max_depth=5):
        if depth >= max_depth:
            return
        
        # Tambah ruangan baru dengan peluang tertentu
        if random.random() < 0.6 and len(self.children) < 4:
            room_types = ["monster"] * 3 + ["treasure"] + ["empty"] * 2
            if depth == max_depth - 1:
                room_types = ["exit"]  # Ruangan terakhir adalah exit
            new_type = random.choice(room_types)
            new_name = f"{self.name}.{len(self.children)+1}"
            
            # Atur peluang encounter berdasarkan jenis ruangan
            encounter = 0.7 if new_type == "monster" else 0.1 if new_type == "treasure" else 0.3
            
            new_room = DungeonNode(new_name, new_type, encounter)
            
            # Tambahkan loot untuk ruangan treasure
            if new_type == "treasure":
                loot_types = ["gold", "weapon", "armor", "potion"]
                new_room.loot = random.choice(loot_types)
            
            self.children.append(new_room)
        
        # Eksplorasi ruangan anak
        for child in self.children:
            child.explore(depth + 1, max_depth)
    
    # Cetak struktur dungeon
    def print_map(self, level=0):
        prefix = "  " * level
        status = "(V)" if self.visited else "(U)"
        print(f"{prefix}{status} {self.name} [{self.room_type}]", end="")
        if self.loot:
            print(f" - Loot: {self.loot}", end="")
        print()
        for child in self.children:
            child.print_map(level + 1)
    
    # Cari ruangan berdasarkan nama
    def find_room(self, name):
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_room(name)
            if found:
                return found
        return None
    
    # Eksplorasi ruangan tertentu
    def visit_room(self, name):
        room = self.find_room(name)
        if room:
            room.visited = True
            # Hasilkan event berdasarkan jenis ruangan
            if room.room_type == "monster" and random.random() < room.encounter_chance:
                monsters = ["Goblin", "Orc", "Skeleton", "Spider"]
                print(f"You encountered a {random.choice(monsters)}!")
                return "fight"
            elif room.room_type == "treasure" and room.loot:
                print(f"You found {room.loot}!")
                room.loot = None  # Harta sudah diambil
                return "treasure"
            elif room.room_type == "exit":
                print("You found the exit!")
                return "exit"
            else:
                print("This room is empty.")
                return "empty"
        return None

# Menu interaktif
def dungeon_game():
    dungeon = DungeonNode("Entrance", "start", 0)
    dungeon.explore(max_depth=5)
    current_room = dungeon
    
    print("Welcome to the Dungeon Explorer!")
    
    while True:
        print("\nCurrent room:", current_room.name)
        print("Type:", current_room.room_type)
        if current_room.visited:
            print("Status: Visited")
        else:
            print("Status: Unvisited")
        
        print("\nMenu:")
        print("1. Explore current room")
        print("2. Move to connected room")
        print("3. View dungeon map")
        print("4. Restart dungeon")
        print("5. Exit game")
        
        choice = input("Choose [1-5]: ")
        
        if choice == '1':
            result = current_room.visit_room(current_room.name)
            # Anda bisa menambahkan logika pertarungan atau pengumpulan harta di sini
        
        elif choice == '2':
            if not current_room.children:
                print("No connected rooms! Explore this room first.")
                continue
            
            print("Connected rooms:")
            for i, room in enumerate(current_room.children, 1):
                print(f"{i}. {room.name} [{room.room_type}]")
            
            try:
                room_choice = int(input("Choose room to move to: ")) - 1
                if 0 <= room_choice < len(current_room.children):
                    current_room = current_room.children[room_choice]
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
        
        elif choice == '3':
            print("\nDungeon Map:")
            dungeon.print_map()
            print("\nLegend: (V) = Visited, (U) = Unvisited")
        
        elif choice == '4':
            dungeon = DungeonNode("Entrance", "start", 0)
            dungeon.explore(max_depth=5)
            current_room = dungeon
            print("New dungeon generated!")
        
        elif choice == '5':
            print("Thanks for playing!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    dungeon_game()