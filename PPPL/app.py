#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplikasi Manajemen Proyek dengan GUI
Fitur:
- Manajemen tim
- Penugasan tugas
- Tracking progress
- Notifikasi deadline
- Visualisasi data
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Dict, Optional, Tuple


class ProjectManager:
    """Class untuk mengelola database proyek"""
    
    def __init__(self, db_name: str = "project_manager.db"):
        """Inisialisasi database"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialize_db()
    
    def _initialize_db(self) -> None:
        """Membuat tabel jika belum ada"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                deadline TEXT,
                status TEXT DEFAULT 'pending',
                progress INTEGER DEFAULT 0
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                role TEXT,
                skills TEXT
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                assigned_to INTEGER,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'todo',
                created_at TEXT,
                deadline TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (assigned_to) REFERENCES team_members (id)
            )
        """)
        
        self.conn.commit()
    
    # CRUD Projects
    def add_project(
        self,
        name: str,
        description: str = "",
        start_date: Optional[str] = None,
        deadline: Optional[str] = None
    ) -> int:
        """Menambahkan proyek baru"""
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
        
        self.cursor.execute("""
            INSERT INTO projects (name, description, start_date, deadline)
            VALUES (?, ?, ?, ?)
        """, (name, description, start_date, deadline))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_projects(self, status: Optional[str] = None) -> List[Dict]:
        """Mendapatkan daftar proyek"""
        query = "SELECT * FROM projects"
        params = ()
        
        if status:
            query += " WHERE status = ?"
            params = (status,)
        
        self.cursor.execute(query, params)
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def update_project_status(self, project_id: int, status: str) -> bool:
        """Mengupdate status proyek"""
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if status not in valid_statuses:
            return False
        
        self.cursor.execute("""
            UPDATE projects SET status = ? WHERE id = ?
        """, (status, project_id))
        
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    # CRUD Team Members
    def add_team_member(
        self,
        name: str,
        email: str = "",
        role: str = "",
        skills: str = ""
    ) -> int:
        """Menambahkan anggota tim baru"""
        self.cursor.execute("""
            INSERT INTO team_members (name, email, role, skills)
            VALUES (?, ?, ?, ?)
        """, (name, email, role, skills))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_team_members(self) -> List[Dict]:
        """Mendapatkan daftar anggota tim"""
        self.cursor.execute("SELECT * FROM team_members")
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    # CRUD Tasks
    def add_task(
        self,
        project_id: int,
        title: str,
        assigned_to: Optional[int] = None,
        description: str = "",
        priority: str = "medium",
        deadline: Optional[str] = None
    ) -> int:
        """Menambahkan tugas baru"""
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.cursor.execute("""
            INSERT INTO tasks (
                project_id, title, description, assigned_to, 
                priority, created_at, deadline
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (project_id, title, description, assigned_to, 
              priority, created_at, deadline))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_tasks(
        self,
        project_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """Mendapatkan daftar tugas"""
        query = """
            SELECT t.*, m.name as assigned_name, p.name as project_name
            FROM tasks t
            LEFT JOIN team_members m ON t.assigned_to = m.id
            LEFT JOIN projects p ON t.project_id = p.id
        """
        params = []
        
        conditions = []
        if project_id:
            conditions.append("t.project_id = ?")
            params.append(project_id)
        if status:
            conditions.append("t.status = ?")
            params.append(status)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        self.cursor.execute(query, params)
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        """Mengupdate status tugas"""
        valid_statuses = ['todo', 'in_progress', 'completed', 'blocked']
        if status not in valid_statuses:
            return False
        
        self.cursor.execute("""
            UPDATE tasks SET status = ? WHERE id = ?
        """, (status, task_id))
        
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    # Analytics
    def get_project_progress(self) -> List[Tuple[str, int]]:
        """Mendapatkan progress proyek untuk visualisasi"""
        self.cursor.execute("""
            SELECT name, progress FROM projects WHERE status != 'completed'
        """)
        return self.cursor.fetchall()
    
    def get_task_distribution(self) -> Dict[str, int]:
        """Mendapatkan distribusi status tugas"""
        self.cursor.execute("""
            SELECT status, COUNT(*) as count FROM tasks GROUP BY status
        """)
        return dict(self.cursor.fetchall())
    
    def get_upcoming_deadlines(self, days: int = 7) -> List[Dict]:
        """Mendapatkan deadline yang akan datang"""
        end_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        
        self.cursor.execute("""
            SELECT t.id, t.title, t.deadline, p.name as project_name
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            WHERE t.deadline BETWEEN date('now') AND ?
            AND t.status != 'completed'
            ORDER BY t.deadline
        """, (end_date,))
        
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def close(self) -> None:
        """Menutup koneksi database"""
        self.conn.close()


class ProjectManagerApp:
    """Class untuk GUI aplikasi manajemen proyek"""
    
    def __init__(self, root: tk.Tk):
        """Inisialisasi GUI"""
        self.root = root
        self.root.title("Manajemen Proyek")
        self.root.geometry("1200x800")
        
        self.db = ProjectManager()
        
        # Style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook (Tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self._create_dashboard_tab()
        self._create_projects_tab()
        self._create_tasks_tab()
        self._create_team_tab()
        self._create_analytics_tab()
        
        # Load initial data
        self.refresh_data()
    
    def _create_dashboard_tab(self) -> None:
        """Membuat tab dashboard"""
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        
        # Upcoming deadlines
        deadline_frame = ttk.LabelFrame(self.dashboard_tab, text="Deadline Mendatang")
        deadline_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.deadline_tree = ttk.Treeview(
            deadline_frame,
            columns=('task', 'project', 'deadline'),
            show='headings'
        )
        self.deadline_tree.heading('task', text='Tugas')
        self.deadline_tree.heading('project', text='Proyek')
        self.deadline_tree.heading('deadline', text='Deadline')
        self.deadline_tree.pack(fill=tk.BOTH, expand=True)
        
        # Project progress
        progress_frame = ttk.LabelFrame(self.dashboard_tab, text="Progress Proyek")
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.progress_canvas_frame = ttk.Frame(progress_frame)
        self.progress_canvas_frame.pack(fill=tk.BOTH, expand=True)
    
    def _create_projects_tab(self) -> None:
        """Membuat tab proyek"""
        self.projects_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.projects_tab, text="Proyek")
        
        # Project list
        project_list_frame = ttk.Frame(self.projects_tab)
        project_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.project_tree = ttk.Treeview(
            project_list_frame,
            columns=('name', 'status', 'progress', 'start_date', 'deadline'),
            show='headings'
        )
        self.project_tree.heading('name', text='Nama Proyek')
        self.project_tree.heading('status', text='Status')
        self.project_tree.heading('progress', text='Progress (%)')
        self.project_tree.heading('start_date', text='Mulai')
        self.project_tree.heading('deadline', text='Deadline')
        self.project_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(
            project_list_frame, 
            orient=tk.VERTICAL, 
            command=self.project_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_tree.configure(yscrollcommand=scrollbar.set)
        
        # Project controls
        control_frame = ttk.Frame(self.projects_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            control_frame, 
            text="Tambah Proyek", 
            command=self._show_add_project_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="Refresh",
            command=self.refresh_data
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_tasks_tab(self) -> None:
        """Membuat tab tugas"""
        self.tasks_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tasks_tab, text="Tugas")
        
        # Task list
        task_list_frame = ttk.Frame(self.tasks_tab)
        task_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.task_tree = ttk.Treeview(
            task_list_frame,
            columns=('title', 'project', 'assigned', 'priority', 'status', 'deadline'),
            show='headings'
        )
        self.task_tree.heading('title', text='Judul Tugas')
        self.task_tree.heading('project', text='Proyek')
        self.task_tree.heading('assigned', text='Ditugaskan ke')
        self.task_tree.heading('priority', text='Prioritas')
        self.task_tree.heading('status', text='Status')
        self.task_tree.heading('deadline', text='Deadline')
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(
            task_list_frame, 
            orient=tk.VERTICAL, 
            command=self.task_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Task controls
        control_frame = ttk.Frame(self.tasks_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            control_frame, 
            text="Tambah Tugas", 
            command=self._show_add_task_dialog
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="Update Status",
            command=self._update_task_status
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_team_tab(self) -> None:
        """Membuat tab tim"""
        self.team_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.team_tab, text="Tim")
        
        # Team list
        team_list_frame = ttk.Frame(self.team_tab)
        team_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.team_tree = ttk.Treeview(
            team_list_frame,
            columns=('name', 'email', 'role', 'skills'),
            show='headings'
        )
        self.team_tree.heading('name', text='Nama')
        self.team_tree.heading('email', text='Email')
        self.team_tree.heading('role', text='Peran')
        self.team_tree.heading('skills', text='Keahlian')
        self.team_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(
            team_list_frame, 
            orient=tk.VERTICAL, 
            command=self.team_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.team_tree.configure(yscrollcommand=scrollbar.set)
        
        # Team controls
        control_frame = ttk.Frame(self.team_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            control_frame, 
            text="Tambah Anggota", 
            command=self._show_add_member_dialog
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_analytics_tab(self) -> None:
        """Membuat tab analitik"""
        self.analytics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analytics_tab, text="Analitik")
        
        # Progress chart
        progress_frame = ttk.LabelFrame(self.analytics_tab, text="Progress Proyek")
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.progress_chart_frame = ttk.Frame(progress_frame)
        self.progress_chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Task distribution chart
        dist_frame = ttk.LabelFrame(self.analytics_tab, text="Distribusi Tugas")
        dist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dist_chart_frame = ttk.Frame(dist_frame)
        self.dist_chart_frame.pack(fill=tk.BOTH, expand=True)
    
    def refresh_data(self) -> None:
        """Memperbarui semua data"""
        self._refresh_projects()
        self._refresh_tasks()
        self._refresh_team()
        self._refresh_deadlines()
        self._refresh_charts()
    
    def _refresh_projects(self) -> None:
        """Memperbarui daftar proyek"""
        for item in self.project_tree.get_children():
            self.project_tree.delete(item)
        
        projects = self.db.get_projects()
        for project in projects:
            self.project_tree.insert('', tk.END, values=(
                project['name'],
                project['status'].replace('_', ' ').title(),
                project['progress'],
                project['start_date'],
                project['deadline']
            ))
    
    def _refresh_tasks(self) -> None:
        """Memperbarui daftar tugas"""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        tasks = self.db.get_tasks()
        for task in tasks:
            self.task_tree.insert('', tk.END, values=(
                task['title'],
                task['project_name'],
                task['assigned_name'] if task['assigned_name'] else '-',
                task['priority'].title(),
                task['status'].replace('_', ' ').title(),
                task['deadline']
            ))
    
    def _refresh_team(self) -> None:
        """Memperbarui daftar tim"""
        for item in self.team_tree.get_children():
            self.team_tree.delete(item)
        
        members = self.db.get_team_members()
        for member in members:
            self.team_tree.insert('', tk.END, values=(
                member['name'],
                member['email'],
                member['role'],
                member['skills']
            ))
    
    def _refresh_deadlines(self) -> None:
        """Memperbarui daftar deadline"""
        for item in self.deadline_tree.get_children():
            self.deadline_tree.delete(item)
        
        deadlines = self.db.get_upcoming_deadlines()
        for task in deadlines:
            self.deadline_tree.insert('', tk.END, values=(
                task['title'],
                task['project_name'],
                task['deadline']
            ))
    
    def _refresh_charts(self) -> None:
        """Memperbarui chart visualisasi"""
        # Hapus chart sebelumnya
        for widget in self.progress_chart_frame.winfo_children():
            widget.destroy()
        
        for widget in self.dist_chart_frame.winfo_children():
            widget.destroy()
        
        for widget in self.progress_canvas_frame.winfo_children():
            widget.destroy()
        
        # Buat progress chart
        project_progress = self.db.get_project_progress()
        if project_progress:
            fig, ax = plt.subplots(figsize=(8, 4))
            project_names = [p[0] for p in project_progress]
            progress = [p[1] for p in project_progress]
            
            bars = ax.barh(project_names, progress, color='skyblue')
            ax.bar_label(bars, fmt='%d%%', padding=3)
            ax.set_xlim(0, 100)
            ax.set_title('Progress Proyek')
            
            canvas = FigureCanvasTkAgg(fig, master=self.progress_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Progress chart untuk dashboard
            fig_dash, ax_dash = plt.subplots(figsize=(8, 2))
            bars_dash = ax_dash.barh(project_names, progress, color='lightgreen')
            ax_dash.bar_label(bars_dash, fmt='%d%%', padding=3)
            ax_dash.set_xlim(0, 100)
            
            canvas_dash = FigureCanvasTkAgg(fig_dash, master=self.progress_canvas_frame)
            canvas_dash.draw()
            canvas_dash.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Buat task distribution chart
        task_dist = self.db.get_task_distribution()
        if task_dist:
            fig, ax = plt.subplots(figsize=(8, 4))
            statuses = [s.replace('_', ' ').title() for s in task_dist.keys()]
            counts = list(task_dist.values())
            
            wedges, texts, autotexts = ax.pie(
                counts, 
                labels=statuses,
                autopct='%1.1f%%',
                startangle=90,
                colors=['#ff9999','#66b3ff','#99ff99','#ffcc99']
            )
            ax.set_title('Distribusi Status Tugas')
            ax.axis('equal')
            
            canvas = FigureCanvasTkAgg(fig, master=self.dist_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _show_add_project_dialog(self) -> None:
        """Menampilkan dialog tambah proyek"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tambah Proyek Baru")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Nama Proyek:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Deskripsi:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        desc_text = tk.Text(dialog, width=30, height=5)
        desc_text.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Tanggal Mulai (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        start_entry = ttk.Entry(dialog, width=15)
        start_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        start_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        ttk.Label(dialog, text="Deadline (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        deadline_entry = ttk.Entry(dialog, width=15)
        deadline_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        def save_project():
            name = name_entry.get()
            description = desc_text.get("1.0", tk.END).strip()
            start_date = start_entry.get()
            deadline = deadline_entry.get() or None
            
            if not name:
                messagebox.showerror("Error", "Nama proyek harus diisi")
                return
            
            try:
                self.db.add_project(name, description, start_date, deadline)
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Sukses", "Proyek berhasil ditambahkan")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menambahkan proyek: {str(e)}")
        
        ttk.Button(dialog, text="Simpan", command=save_project).grid(row=4, column=1, padx=5, pady=10, sticky=tk.E)
    
    def _show_add_task_dialog(self) -> None:
        """Menampilkan dialog tambah tugas"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tambah Tugas Baru")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        
        # Get projects and team members for dropdowns
        projects = self.db.get_projects()
        members = self.db.get_team_members()
        
        ttk.Label(dialog, text="Proyek:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        project_var = tk.StringVar()
        project_combo = ttk.Combobox(dialog, textvariable=project_var, width=40)
        project_combo['values'] = [p['name'] for p in projects]
        project_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Judul Tugas:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Deskripsi:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        desc_text = tk.Text(dialog, width=30, height=5)
        desc_text.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Ditugaskan ke:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(dialog, textvariable=member_var, width=40)
        member_combo['values'] = [m['name'] for m in members]
        member_combo.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Prioritas:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        priority_var = tk.StringVar(value="medium")
        ttk.Radiobutton(dialog, text="Rendah", variable=priority_var, value="low").grid(row=4, column=1, sticky=tk.W)
        ttk.Radiobutton(dialog, text="Sedang", variable=priority_var, value="medium").grid(row=5, column=1, sticky=tk.W)
        ttk.Radiobutton(dialog, text="Tinggi", variable=priority_var, value="high").grid(row=6, column=1, sticky=tk.W)
        
        ttk.Label(dialog, text="Deadline (YYYY-MM-DD):").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        deadline_entry = ttk.Entry(dialog, width=15)
        deadline_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        
        def save_task():
            project_name = project_var.get()
            title = title_entry.get()
            description = desc_text.get("1.0", tk.END).strip()
            member_name = member_var.get()
            priority = priority_var.get()
            deadline = deadline_entry.get() or None
            
            if not project_name or not title:
                messagebox.showerror("Error", "Proyek dan judul tugas harus diisi")
                return
            
            # Find project ID
            project_id = next((p['id'] for p in projects if p['name'] == project_name), None)
            if not project_id:
                messagebox.showerror("Error", "Proyek tidak ditemukan")
                return
            
            # Find member ID (optional)
            member_id = None
            if member_name:
                member_id = next((m['id'] for m in members if m['name'] == member_name), None)
                if not member_id:
                    messagebox.showerror("Error", "Anggota tim tidak ditemukan")
                    return
            
            try:
                self.db.add_task(
                    project_id,
                    title,
                    member_id,
                    description,
                    priority,
                    deadline
                )
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Sukses", "Tugas berhasil ditambahkan")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menambahkan tugas: {str(e)}")
        
        ttk.Button(dialog, text="Simpan", command=save_task).grid(row=8, column=1, padx=5, pady=10, sticky=tk.E)
    
    def _show_add_member_dialog(self) -> None:
        """Menampilkan dialog tambah anggota tim"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tambah Anggota Tim")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Nama:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        email_entry = ttk.Entry(dialog, width=30)
        email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Peran:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        role_entry = ttk.Entry(dialog, width=30)
        role_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Keahlian:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        skills_entry = ttk.Entry(dialog, width=30)
        skills_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def save_member():
            name = name_entry.get()
            email = email_entry.get()
            role = role_entry.get()
            skills = skills_entry.get()
            
            if not name:
                messagebox.showerror("Error", "Nama harus diisi")
                return
            
            try:
                self.db.add_team_member(name, email, role, skills)
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Sukses", "Anggota tim berhasil ditambahkan")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menambahkan anggota tim: {str(e)}")
        
        ttk.Button(dialog, text="Simpan", command=save_member).grid(row=4, column=1, padx=5, pady=10, sticky=tk.E)
    
    def _update_task_status(self) -> None:
        """Menampilkan dialog update status tugas"""
        selected = self.task_tree.focus()
        if not selected:
            messagebox.showwarning("Peringatan", "Tidak ada tugas yang dipilih")
            return
        
        item = self.task_tree.item(selected)
        task_id = item['values'][0]  # Asumsi ID adalah nilai pertama
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Status Tugas")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text="Pilih Status:").pack(pady=10)
        
        status_var = tk.StringVar(value="in_progress")
        
        ttk.Radiobutton(dialog, text="To Do", variable=status_var, value="todo").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="In Progress", variable=status_var, value="in_progress").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Completed", variable=status_var, value="completed").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Blocked", variable=status_var, value="blocked").pack(anchor=tk.W, padx=20)
        
        def update_status():
            status = status_var.get()
            if self.db.update_task_status(task_id, status):
                self.refresh_data()
                dialog.destroy()
                messagebox.showinfo("Sukses", "Status tugas berhasil diupdate")
            else:
                messagebox.showerror("Error", "Gagal mengupdate status tugas")
        
        ttk.Button(dialog, text="Update", command=update_status).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManagerApp(root)
    root.mainloop()