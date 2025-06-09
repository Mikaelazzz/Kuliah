import json
import os
from typing import List, Dict, Optional


class TaskManager:
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict[str, str]]:
        if not os.path.exists(self.filename):
            return []
        
        with open(self.filename, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    
    def _save_tasks(self) -> None:
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, indent=4)
    
    def add_task(self, title: str, description: str = "") -> Dict[str, str]:
        if not title:
            raise ValueError("Judul tugas tidak boleh kosong")
        
        task = {
            'id': str(len(self.tasks) + 1),
            'title': title,
            'description': description,
            'completed': False
        }
        
        self.tasks.append(task)
        self._save_tasks()
        return task
    
    def list_tasks(self, completed: Optional[bool] = None) -> List[Dict[str, str]]:
        if completed is None:
            return self.tasks
        
        return [task for task in self.tasks if task['completed'] == completed]
    
    def complete_task(self, task_id: str) -> Optional[Dict[str, str]]:
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self._save_tasks()
                return task
        return None
    
    def delete_task(self, task_id: str) -> bool:
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        
        if len(self.tasks) < initial_length:
            self._save_tasks()
            return True
        return False


def display_menu() -> None:
    print("\n=== Aplikasi Manajemen Tugas ===")
    print("1. Tambah Tugas Baru")
    print("2. Lihat Daftar Tugas")
    print("3. Tandai Tugas Selesai")
    print("4. Hapus Tugas")
    print("5. Keluar")


def get_user_input(prompt: str) -> str:
    return input(prompt).strip()


def main() -> None:
    manager = TaskManager()
    
    while True:
        display_menu()
        choice = get_user_input("Pilih menu (1-5): ")
        
        if choice == '1':
            title = get_user_input("Judul tugas: ")
            description = get_user_input("Deskripsi (opsional): ")
            try:
                task = manager.add_task(title, description)
                print(f"Tugas '{task['title']}' berhasil ditambahkan!")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            print("\nDaftar Tugas:")
            tasks = manager.list_tasks()
            if not tasks:
                print("Tidak ada tugas.")
            else:
                for task in tasks:
                    status = "✓" if task['completed'] else " "
                    print(f"{task['id']}. [{status}] {task['title']}")
                    if task['description']:
                        print(f"   Deskripsi: {task['description']}")
        
        elif choice == '3':
            # Tandai tugas selesai
            task_id = get_user_input("ID tugas yang selesai: ")
            task = manager.complete_task(task_id)
            if task:
                print(f"Tugas '{task['title']}' ditandai selesai!")
            else:
                print("Tugas tidak ditemukan.")
        
        elif choice == '4':
            # Hapus tugas
            task_id = get_user_input("ID tugas yang akan dihapus: ")
            if manager.delete_task(task_id):
                print("Tugas berhasil dihapus!")
            else:
                print("Tugas tidak ditemukan.")
        
        elif choice == '5':
            # Keluar
            print("Terima kasih telah menggunakan aplikasi!")
            break
        
        else:
            print("Pilihan tidak valid. Silakan pilih 1-5.")


if __name__ == "__main__":
    main()