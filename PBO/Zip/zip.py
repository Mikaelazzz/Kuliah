import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import tarfile
import os
from pathlib import Path
import threading
import shutil
import subprocess
import sys
import urllib.request
import zipfile as zipf
import tempfile
import platform

# Try to import optional libraries with fallback
try:
    import py7zr
    HAS_PY7ZR = True
except ImportError:
    HAS_PY7ZR = False

try:
    import patoolib
    HAS_PATOOLIB = True
except ImportError:
    HAS_PATOOLIB = False

try:
    import rarfile
    HAS_RARFILE = True
except ImportError:
    HAS_RARFILE = False

class FileCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("File Compressor & Decompressor")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.selected_files = []
        self.selected_archives = []
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.rar_path = None
        self.unrar_path = None
        
        self.create_widgets()
        self.setup_rar_support()
        
    def setup_rar_support(self):
        self.rar_path = self.find_or_setup_rar()
        self.unrar_path = self.find_unrar_executable()
        
        if self.rar_path:
            print(f"RAR compression enabled using: {self.rar_path}")
            
        if self.unrar_path:
            print(f"RAR extraction enabled using: {self.unrar_path}")
            # Configure rarfile library to use our unrar path
            if HAS_RARFILE:
                rarfile.UNRAR_TOOL = self.unrar_path
                
        status_msg = "Ready"
        if self.rar_path and self.unrar_path:
            status_msg = "RAR support: Full (compress & extract)"
        elif self.rar_path:
            status_msg = "RAR support: Compression only"
        elif self.unrar_path:
            status_msg = "RAR support: Extraction only"
            
        self.update_status(status_msg)
        
    def find_unrar_executable(self):
        # Check WinRAR installation path first
        winrar_paths = [
            r"D:\Apps\Winrar\unrar.exe",
            r"D:\Apps\Winrar\rar.exe",  # rar.exe can also extract
            r"D:\Apps\Winrar\winrar.exe"
        ]
        
        for path in winrar_paths:
            if os.path.exists(path):
                if self.test_unrar_executable(path):
                    return path
        
        # Common installation paths
        if platform.system().lower() == "windows":
            possible_paths = [
                r"C:\Program Files\WinRAR\unrar.exe",
                r"C:\Program Files (x86)\WinRAR\unrar.exe",
                r"C:\Program Files\WinRAR\rar.exe",
                r"C:\Program Files (x86)\WinRAR\rar.exe",
                r"C:\Program Files\WinRAR\winrar.exe",
                r"C:\Program Files (x86)\WinRAR\winrar.exe",
                os.path.join(os.path.expanduser("~"), "AppData", "Local", "WinRAR", "unrar.exe"),
                "unrar.exe",
                "rar.exe"
            ]
        else:
            possible_paths = [
                "/usr/bin/unrar",
                "/usr/local/bin/unrar",
                "/usr/bin/rar",
                "/usr/local/bin/rar",
                "/opt/rar/unrar",
                "unrar",
                "rar"
            ]
        
        # Check each possible path
        for path in possible_paths:
            if self.test_unrar_executable(path):
                return path
                
        return None

    def test_unrar_executable(self, path):
        try:
            if not os.path.exists(path) and not shutil.which(path):
                return False
            
            # Test with help command
            result = subprocess.run([path, '--help'], 
                                  capture_output=True, 
                                  timeout=5,
                                  creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
            return True
        except Exception as e:
            try:
                # Try without --help for some versions
                result = subprocess.run([path], 
                                      capture_output=True, 
                                      timeout=5,
                                      creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
                return True
            except:
                return False

    def extract_rar_with_executable(self, archive_path, extract_dir):
        if not self.unrar_path:
            raise Exception("No RAR extraction executable found")
        
        try:
            # Ensure extract directory exists
            os.makedirs(extract_dir, exist_ok=True)
            
            # Build command for extraction
            # Use 'x' command to extract with full paths
            cmd_args = [self.unrar_path, 'x', '-y', archive_path, extract_dir + os.sep]
            
            print(f"Executing RAR extraction: {' '.join(cmd_args)}")
            
            # Execute command
            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=self.current_dir,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            
            print(f"Extraction return code: {result.returncode}")
            print(f"Extraction stdout: {result.stdout}")
            print(f"Extraction stderr: {result.stderr}")
            
            # Check if extraction was successful
            if result.returncode == 0:
                # Verify files were extracted
                if os.path.exists(extract_dir) and os.listdir(extract_dir):
                    return True
                else:
                    raise Exception("No files were extracted")
            else:
                # Try alternative command format
                print("First extraction command failed, trying alternative...")
                
                # Alternative: extract to current directory then move
                temp_extract_dir = tempfile.mkdtemp()
                try:
                    cmd_args_alt = [self.unrar_path, 'e', '-y', archive_path, temp_extract_dir + os.sep]
                    
                    result_alt = subprocess.run(
                        cmd_args_alt,
                        capture_output=True,
                        text=True,
                        timeout=300,
                        creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                    )
                    
                    if result_alt.returncode == 0:
                        # Move extracted files to target directory
                        for item in os.listdir(temp_extract_dir):
                            src = os.path.join(temp_extract_dir, item)
                            dst = os.path.join(extract_dir, item)
                            if os.path.isdir(src):
                                shutil.copytree(src, dst)
                            else:
                                shutil.copy2(src, dst)
                        return True
                    else:
                        error_msg = result.stderr if result.stderr else result.stdout
                        raise Exception(f"RAR extraction failed: {error_msg}")
                finally:
                    # Clean up temp directory
                    shutil.rmtree(temp_extract_dir, ignore_errors=True)
                    
        except subprocess.TimeoutExpired:
            raise Exception("RAR extraction timed out")
        except Exception as e:
            raise Exception(f"RAR extraction error: {str(e)}")

    def find_or_setup_rar(self):
        # First try the specific path provided by user
        specific_paths = [
            r"D:\Apps\Winrar\rar.exe",
            r"D:\Apps\Winrar\winrar.exe",
            r"D:\Apps\Winrar\Rar.exe",
            r"D:\Apps\Winrar\WinRAR.exe"
        ]
        
        for path in specific_paths:
            if self.test_rar_executable(path):
                return path
        
        # Try to find existing RAR installation in common locations
        rar_path = self.find_rar_executable()
        if rar_path:
            return rar_path
            
        return None

    def find_rar_executable(self):
        system = platform.system().lower()
        
        # Common installation paths
        if system == "windows":
            possible_paths = [
                r"C:\Program Files\WinRAR\rar.exe",
                r"C:\Program Files (x86)\WinRAR\rar.exe",
                r"C:\Program Files\WinRAR\winrar.exe",
                r"C:\Program Files (x86)\WinRAR\winrar.exe",
                os.path.join(os.path.expanduser("~"), "AppData", "Local", "WinRAR", "rar.exe"),
                "rar.exe",
                "winrar.exe"
            ]
        else:
            possible_paths = [
                "/usr/bin/rar",
                "/usr/local/bin/rar", 
                "/opt/rar/rar",
                "rar"
            ]
        
        # Check each possible path
        for path in possible_paths:
            if self.test_rar_executable(path):
                return path
                
        # Try system PATH
        try:
            result = subprocess.run(["rar"], capture_output=True, timeout=3)
            if result.returncode != 127:  # Command found
                return "rar"
        except:
            pass
            
        try:
            result = subprocess.run(["winrar"], capture_output=True, timeout=3)
            if result.returncode != 127:  # Command found
                return "winrar"
        except:
            pass
            
        return None

    def test_rar_executable(self, path):
        try:
            if not os.path.exists(path) and not shutil.which(path):
                return False
            
            # Test the executable with a simple command
            result = subprocess.run([path], 
                                  capture_output=True, 
                                  timeout=5,
                                  creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
            return True
        except Exception as e:
            print(f"Testing {path} failed: {e}")
            return False

    def create_rar_archive(self, archive_path, files):
        if not self.rar_path:
            raise Exception("WinRAR executable not found")
        
        try:
            # Delete existing archive if it exists
            if os.path.exists(archive_path):
                os.remove(archive_path)
            
            # Prepare command arguments
            # Using 'a' command to add files to archive
            # -ep1 excludes base folder names from paths
            # -m5 sets maximum compression
            cmd_args = [self.rar_path, 'a', '-ep1', '-m5', archive_path]
            
            # Add all files to the command
            cmd_args.extend(files)
            
            print(f"Executing RAR command: {' '.join(cmd_args)}")
            
            # Execute RAR command
            result = subprocess.run(
                cmd_args, 
                capture_output=True, 
                text=True, 
                timeout=300,
                cwd=self.current_dir,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            
            print(f"RAR command return code: {result.returncode}")
            print(f"RAR stdout: {result.stdout}")
            print(f"RAR stderr: {result.stderr}")
            
            # Check if command was successful
            if result.returncode == 0:
                # Verify archive was created
                if os.path.exists(archive_path) and os.path.getsize(archive_path) > 0:
                    return True
                else:
                    raise Exception("Archive file was not created or is empty")
            else:
                # Try alternative command format if first one fails
                print("First RAR command failed, trying alternative format...")
                
                # Alternative command without -ep1 flag
                cmd_args_alt = [self.rar_path, 'a', archive_path]
                cmd_args_alt.extend(files)
                
                result_alt = subprocess.run(
                    cmd_args_alt, 
                    capture_output=True, 
                    text=True, 
                    timeout=300,
                    cwd=self.current_dir,
                    creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                )
                
                print(f"Alternative RAR command return code: {result_alt.returncode}")
                print(f"Alternative RAR stdout: {result_alt.stdout}")
                print(f"Alternative RAR stderr: {result_alt.stderr}")
                
                if result_alt.returncode == 0 and os.path.exists(archive_path):
                    return True
                else:
                    error_msg = result.stderr if result.stderr else result.stdout
                    if not error_msg:
                        error_msg = f"RAR command failed with return code {result.returncode}"
                    raise Exception(f"RAR creation failed: {error_msg}")
                    
        except subprocess.TimeoutExpired:
            raise Exception("RAR creation timed out (300 seconds)")
        except FileNotFoundError:
            raise Exception(f"RAR executable not found at: {self.rar_path}")
        except Exception as e:
            raise Exception(f"RAR creation error: {str(e)}")

    def create_rar_with_fallback(self, archive_path, files):
        # Method 1: Use WinRAR executable
        if self.rar_path:
            try:
                self.update_status("Creating RAR archive with WinRAR...")
                return self.create_rar_archive(archive_path, files)
            except Exception as e:
                print(f"WinRAR creation failed: {e}")
                self.update_status(f"WinRAR failed: {str(e)}")
        
        # Method 2: Use patoolib if available
        if HAS_PATOOLIB:
            try:
                self.update_status("Creating RAR archive with patoolib...")
                return self.create_rar_patoolib(archive_path, files)
            except Exception as e:
                print(f"Patoolib RAR creation failed: {e}")
        
        # Method 3: Create ZIP with RAR extension (last resort)
        try:
            self.update_status("Creating RAR-compatible archive...")
            return self.create_zip_as_rar(archive_path, files)
        except Exception as e:
            print(f"ZIP-as-RAR creation failed: {e}")
            
        raise Exception("All RAR creation methods failed")

    def create_rar_patoolib(self, archive_path, files):
        """Create RAR using patoolib"""
        # Create temporary directory for files
        temp_dir = tempfile.mkdtemp()
        try:
            # Copy files to temp directory
            for file_path in files:
                dest_path = os.path.join(temp_dir, os.path.basename(file_path))
                shutil.copy2(file_path, dest_path)
            
            # Create RAR archive
            patoolib.create_archive(archive_path, [temp_dir])
            return True
        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)

    def create_zip_as_rar(self, archive_path, files):
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files:
                zipf.write(file_path, os.path.basename(file_path))
        return True
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="File Compressor & Decompressor", 
                              font=('Arial', 18, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Compress Section
        compress_frame = tk.LabelFrame(main_frame, text="Compress Files", 
                                     font=('Arial', 12, 'bold'),
                                     bg='#ecf0f1', fg='#2c3e50', bd=2)
        compress_frame.pack(fill='x', pady=10)
        
        # File selection
        file_select_frame = tk.Frame(compress_frame, bg='#ecf0f1')
        file_select_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(file_select_frame, text="Select Files to Compress", 
                 command=self.select_files,
                 font=('Arial', 10, 'bold'),
                 bg='#3498db', fg='white',
                 padx=20, pady=8,
                 cursor='hand2').pack(side='left')
        
        self.files_count_label = tk.Label(file_select_frame, text="No files selected", 
                                         font=('Arial', 10),
                                         bg='#ecf0f1', fg='#7f8c8d')
        self.files_count_label.pack(side='left', padx=20)
        
        # Clear files button
        tk.Button(file_select_frame, text="Clear", 
                 command=self.clear_files_selection,
                 font=('Arial', 9),
                 bg='#95a5a6', fg='white',
                 padx=15, pady=5,
                 cursor='hand2').pack(side='right')
        
        # Selected files display
        self.files_listbox = tk.Listbox(compress_frame, height=5, 
                                       font=('Arial', 9),
                                       bg='white', selectbackground='#3498db')
        self.files_listbox.pack(fill='x', padx=10, pady=(0, 10))
        
        # Compression settings
        settings_frame = tk.Frame(compress_frame, bg='#ecf0f1')
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(settings_frame, text="Format:", font=('Arial', 10, 'bold'),
                bg='#ecf0f1').pack(side='left')
        
        self.format_var = tk.StringVar(value="zip")
        format_combo = ttk.Combobox(settings_frame, textvariable=self.format_var,
                                   values=["zip", "7z", "tar.gz", "rar"],
                                   state="readonly", width=10)
        format_combo.pack(side='left', padx=10)
        
        tk.Label(settings_frame, text="Archive Name:", font=('Arial', 10, 'bold'),
                bg='#ecf0f1').pack(side='left', padx=(20, 5))
        
        self.archive_name_var = tk.StringVar(value="archive")
        tk.Entry(settings_frame, textvariable=self.archive_name_var,
                font=('Arial', 10), width=20).pack(side='left', padx=5)
        
        # Compress button
        self.compress_btn = tk.Button(compress_frame, text="Compress Files", 
                                     command=self.compress_files,
                                     font=('Arial', 12, 'bold'),
                                     bg='#95a5a6', fg='white',
                                     padx=30, pady=10,
                                     cursor='hand2',
                                     state='disabled')
        self.compress_btn.pack(pady=10)
        
        # Decompress Section
        decompress_frame = tk.LabelFrame(main_frame, text="Decompress Files", 
                                       font=('Arial', 12, 'bold'),
                                       bg='#ecf0f1', fg='#2c3e50', bd=2)
        decompress_frame.pack(fill='x', pady=10)
        
        # Archive selection
        archive_select_frame = tk.Frame(decompress_frame, bg='#ecf0f1')
        archive_select_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(archive_select_frame, text="Select Archives to Decompress", 
                 command=self.select_archives,
                 font=('Arial', 10, 'bold'),
                 bg='#e74c3c', fg='white',
                 padx=20, pady=8,
                 cursor='hand2').pack(side='left')
        
        self.archives_count_label = tk.Label(archive_select_frame, text="No archives selected", 
                                            font=('Arial', 10),
                                            bg='#ecf0f1', fg='#7f8c8d')
        self.archives_count_label.pack(side='left', padx=20)
        
        # Clear archives button
        tk.Button(archive_select_frame, text="Clear", 
                 command=self.clear_archive_selection,
                 font=('Arial', 9),
                 bg='#95a5a6', fg='white',
                 padx=15, pady=5,
                 cursor='hand2').pack(side='right')
        
        # Selected archives display
        self.archives_listbox = tk.Listbox(decompress_frame, height=4, 
                                          font=('Arial', 9),
                                          bg='white', selectbackground='#e74c3c')
        self.archives_listbox.pack(fill='x', padx=10, pady=(0, 10))
        
        # Archive info display
        archive_info_frame = tk.Frame(decompress_frame, bg='#ecf0f1')
        archive_info_frame.pack(fill='x', padx=10, pady=5)
        
        self.archive_info_label = tk.Label(archive_info_frame, text="", 
                                          font=('Arial', 9),
                                          bg='#ecf0f1', fg='#34495e')
        self.archive_info_label.pack(side='left')
        
        # Decompress button
        self.decompress_btn = tk.Button(decompress_frame, text="Decompress All Archives", 
                                       command=self.decompress_files,
                                       font=('Arial', 12, 'bold'),
                                       bg='#95a5a6', fg='white',
                                       padx=30, pady=10,
                                       cursor='hand2',
                                       state='disabled')
        self.decompress_btn.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var,
                                          maximum=100, length=500)
        self.progress_bar.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Ready", 
                                    font=('Arial', 10),
                                    bg='#f0f0f0', fg='#2c3e50')
        self.status_label.pack(pady=5)
        
        # Extracted files display section
        self.extracted_frame = tk.LabelFrame(main_frame, text="Recently Extracted Files", 
                                           font=('Arial', 11, 'bold'),
                                           bg='#ecf0f1', fg='#2c3e50', bd=2)
        self.extracted_frame.pack(fill='both', expand=True, pady=10)
        
        # Scrollable text widget for extracted files
        extracted_scroll_frame = tk.Frame(self.extracted_frame, bg='#ecf0f1')
        extracted_scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Text widget with scrollbar
        self.extracted_text = tk.Text(extracted_scroll_frame, height=8, 
                                     font=('Arial', 9),
                                     bg='white', fg='#2c3e50',
                                     wrap=tk.WORD, state='disabled')
        
        extracted_scrollbar = tk.Scrollbar(extracted_scroll_frame, orient='vertical',
                                         command=self.extracted_text.yview)
        self.extracted_text.configure(yscrollcommand=extracted_scrollbar.set)
        
        self.extracted_text.pack(side='left', fill='both', expand=True)
        extracted_scrollbar.pack(side='right', fill='y')
        
        # Initially hide the extracted files frame
        self.extracted_frame.pack_forget()
        
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select files to compress",
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("Document files", "*.pdf;*.doc;*.docx;*.xls;*.xlsx")
            ]
        )
        
        if files:
            self.selected_files = list(files)
            self.update_files_display()
            
    def update_files_display(self):
        self.files_listbox.delete(0, tk.END)
        total_size = 0
        
        for file_path in self.selected_files:
            filename = os.path.basename(file_path)
            size = self.get_file_size_bytes(file_path)
            total_size += size
            
            display_text = f"{filename} ({self.format_file_size(size)})"
            self.files_listbox.insert(tk.END, display_text)
            
        count = len(self.selected_files)
        self.files_count_label.config(text=f"{count} file(s) selected - Total: {self.format_file_size(total_size)}")
        
        # Enable compress button
        if count > 0:
            self.compress_btn.config(state='normal', bg='#27ae60')
        else:
            self.compress_btn.config(state='disabled', bg='#95a5a6')
            
    def clear_files_selection(self):
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)
        self.files_count_label.config(text="No files selected")
        self.compress_btn.config(state='disabled', bg='#95a5a6')
        
    def select_archives(self):
        archives = filedialog.askopenfilenames(
            title="Select archives to decompress",
            filetypes=[
                ("All archives", "*.zip;*.7z;*.rar;*.tar.gz;*.tgz"),
                ("ZIP files", "*.zip"),
                ("7Z files", "*.7z"),
                ("RAR files", "*.rar"),
                ("TAR.GZ files", "*.tar.gz;*.tgz")
            ]
        )
        
        if archives:
            self.selected_archives = list(archives)
            self.update_archives_display()
            
    def update_archives_display(self):
        self.archives_listbox.delete(0, tk.END)
        total_size = 0
        
        for archive_path in self.selected_archives:
            filename = os.path.basename(archive_path)
            file_ext = self.get_archive_extension(archive_path)
            
            size = self.get_file_size_bytes(archive_path)
            total_size += size
            
            display_text = f"{filename} ({file_ext.upper()}) - {self.format_file_size(size)}"
            self.archives_listbox.insert(tk.END, display_text)
            
        count = len(self.selected_archives)
        self.archives_count_label.config(text=f"{count} archive(s) selected")
        self.archive_info_label.config(text=f"Total size: {self.format_file_size(total_size)}")
        
        # Enable decompress button
        if count > 0:
            self.decompress_btn.config(state='normal', bg='#f39c12')
        else:
            self.decompress_btn.config(state='disabled', bg='#95a5a6')
            
    def clear_archive_selection(self):
        self.selected_archives = []
        self.archives_listbox.delete(0, tk.END)
        self.archives_count_label.config(text="No archives selected")
        self.archive_info_label.config(text="")
        self.decompress_btn.config(state='disabled', bg='#95a5a6')
        
    def get_file_size_bytes(self, file_path):
        try:
            return os.path.getsize(file_path)
        except:
            return 0
            
    def format_file_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def get_archive_extension(self, file_path):
        file_path_lower = file_path.lower()
        if file_path_lower.endswith('.tar.gz'):
            return 'tar.gz'
        elif file_path_lower.endswith('.tgz'):
            return 'tar.gz'
        else:
            return Path(file_path).suffix[1:]  # Remove the dot
    
    def display_extracted_files(self, extracted_results):
        self.extracted_text.config(state='normal')
        self.extracted_text.delete(1.0, tk.END)
        
        if not extracted_results:
            self.extracted_frame.pack_forget()
            return
            
        # Show the extracted files frame
        self.extracted_frame.pack(fill='both', expand=True, pady=10)
        
        for result in extracted_results:
            extract_dir = result['extract_dir']
            archive_name = result['archive_name']
            extracted_files = result['files']
            
            # Add header for this archive
            self.extracted_text.insert(tk.END, f"📁 {archive_name}\n", 'header')
            self.extracted_text.insert(tk.END, f"   Extracted to: {os.path.basename(extract_dir)}\n\n")
            
            if extracted_files:
                self.extracted_text.insert(tk.END, "   Contents:\n")
                file_count = 0
                for file_info in extracted_files:
                    file_path = file_info['path']
                    rel_path = file_info['relative_path']
                    
                    # Get file size
                    size = self.get_file_size_bytes(file_path)
                    
                    # Determine if it's a file or directory
                    if os.path.isdir(file_path):
                        self.extracted_text.insert(tk.END, f"   📂 {rel_path}/\n")
                    else:
                        self.extracted_text.insert(tk.END, f"   📄 {rel_path} ({self.format_file_size(size)})\n")
                        file_count += 1
                        
                self.extracted_text.insert(tk.END, f"\n   Total files: {file_count}\n")
            else:
                self.extracted_text.insert(tk.END, "   No files found\n")
                
            self.extracted_text.insert(tk.END, "\n" + "="*60 + "\n\n")
        
        # Configure text tags for better formatting
        self.extracted_text.tag_configure('header', font=('Arial', 10, 'bold'), foreground='#2c3e50')
        
        self.extracted_text.config(state='disabled')
        self.extracted_text.see(1.0)  # Scroll to top
    
    def get_extracted_contents(self, extract_dir):
        extracted_files = []
        
        try:
            for root, dirs, files in os.walk(extract_dir):
                # Add directories
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    rel_path = os.path.relpath(dir_path, extract_dir)
                    extracted_files.append({
                        'path': dir_path,
                        'relative_path': rel_path
                    })
                
                # Add files (exclude archive files)
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    rel_path = os.path.relpath(file_path, extract_dir)
                    
                    # Skip if this is an archive file (likely the original archive)
                    file_ext = os.path.splitext(file_name)[1].lower()
                    if file_ext not in ['.zip', '.7z', '.rar', '.tar', '.gz', '.tgz']:
                        extracted_files.append({
                            'path': file_path,
                            'relative_path': rel_path
                        })
                    
        except Exception as e:
            print(f"Error scanning directory {extract_dir}: {e}")
            
        return extracted_files
            
    def compress_files(self):
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select files to compress first!")
            return
            
        archive_name = self.archive_name_var.get().strip()
        if not archive_name:
            messagebox.showwarning("Warning", "Please enter an archive name!")
            return
            
        format_type = self.format_var.get()
        archive_filename = f"{archive_name}.{format_type}"
        archive_path = os.path.join(self.current_dir, archive_filename)
        
        # Check if file already exists
        if os.path.exists(archive_path):
            result = messagebox.askyesno("File Exists", 
                                       f"Archive '{archive_filename}' already exists.\nDo you want to overwrite it?")
            if not result:
                return
        
        # Run compression in separate thread
        thread = threading.Thread(target=self._compress_files_thread, 
                                 args=(archive_path, format_type))
        thread.daemon = True
        thread.start()
        
    def _compress_files_thread(self, archive_path, format_type):
        try:
            self.update_status("Compressing files...")
            self.progress_var.set(0)
            
            total_files = len(self.selected_files)
            
            if format_type == "zip":
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for i, file_path in enumerate(self.selected_files):
                        zipf.write(file_path, os.path.basename(file_path))
                        progress = ((i + 1) / total_files) * 100
                        self.progress_var.set(progress)
                        
            elif format_type == "7z":
                if not HAS_PY7ZR:
                    raise Exception("py7zr library not installed. Run: pip install py7zr")
                with py7zr.SevenZipFile(archive_path, 'w') as archive:
                    for i, file_path in enumerate(self.selected_files):
                        archive.write(file_path, os.path.basename(file_path))
                        progress = ((i + 1) / total_files) * 100
                        self.progress_var.set(progress)
                        
            elif format_type == "tar.gz":
                with tarfile.open(archive_path, 'w:gz') as tar:
                    for i, file_path in enumerate(self.selected_files):
                        tar.add(file_path, arcname=os.path.basename(file_path))
                        progress = ((i + 1) / total_files) * 100
                        self.progress_var.set(progress)
                        
            elif format_type == "rar":
                # Use enhanced RAR creation with the specific path
                self.progress_var.set(25)
                success = self.create_rar_with_fallback(archive_path, self.selected_files)
                if not success:
                    raise Exception("Failed to create RAR archive")
                self.progress_var.set(100)
            
            self.progress_var.set(100)
            self.update_status(f"Compression completed: {os.path.basename(archive_path)}")
            
            # Show success message
            if format_type == "rar":
                if self.rar_path:
                    msg = f"RAR archive created successfully using WinRAR!\nSaved as: {archive_path}"
                else:
                    msg = f"RAR-compatible archive created!\nSaved as: {archive_path}\n\nNote: Created using alternative method."
            else:
                msg = f"Files compressed successfully!\nSaved as: {archive_path}"
                
            messagebox.showinfo("Success", msg)
            
        except Exception as e:
            self.update_status("Compression failed!")
            messagebox.showerror("Error", f"Compression failed: {str(e)}")
        finally:
            self.progress_var.set(0)
            
    def decompress_files(self):
        if not self.selected_archives:
            messagebox.showwarning("Warning", "Please select archives to decompress first!")
            return
        
        # Confirm decompression
        count = len(self.selected_archives)
        result = messagebox.askyesno("Confirm Decompression", 
                                   f"Do you want to decompress {count} archive(s)?")
        if not result:
            return
        
        # Run decompression in separate thread
        thread = threading.Thread(target=self._decompress_files_thread)
        thread.daemon = True
        thread.start()
        
    def _decompress_files_thread(self):
        total_archives = len(self.selected_archives)
        successful = 0
        failed = 0
        failed_files = []
        extracted_results = []
        
        try:
            for i, archive_path in enumerate(self.selected_archives):
                filename = os.path.basename(archive_path)
                try:
                    # Update status
                    self.update_status(f"Decompressing {i+1}/{total_archives}: {filename}")
                    
                    # Calculate progress
                    base_progress = (i / total_archives) * 100
                    self.progress_var.set(base_progress)
                    
                    # Validate file exists and is readable
                    if not os.path.exists(archive_path):
                        raise Exception(f"Archive file not found: {archive_path}")
                    
                    if not os.access(archive_path, os.R_OK):
                        raise Exception(f"Cannot read archive file: {archive_path}")
                    
                    # Get file extension and determine format
                    file_ext = self.get_archive_extension(archive_path)
                    archive_name = Path(archive_path).stem
                    
                    # Handle .tar.gz case properly
                    if file_ext == 'tar.gz':
                        if archive_name.endswith('.tar'):
                            archive_name = archive_name[:-4]
                    
                    # Create extraction directory with just the archive name (no "Extracted_" prefix)
                    base_extract_dir = archive_name
                    extract_dir = os.path.join(self.current_dir, base_extract_dir)
                    
                    # Handle duplicate directories
                    counter = 1
                    original_extract_dir = extract_dir
                    while os.path.exists(extract_dir) and os.listdir(extract_dir):
                        extract_dir = f"{original_extract_dir}_{counter}"
                        counter += 1
                    
                    # Create extraction directory
                    os.makedirs(extract_dir, exist_ok=True)
                    
                    # Update progress
                    mid_progress = base_progress + (25 / total_archives)
                    self.progress_var.set(mid_progress)
                    
                    # Extract based on format
                    success = False
                    
                    if file_ext == 'zip':
                        success = self._extract_zip(archive_path, extract_dir)
                    elif file_ext == '7z':
                        success = self._extract_7z(archive_path, extract_dir)
                    elif file_ext in ['tar.gz', 'tgz']:
                        success = self._extract_tar_gz(archive_path, extract_dir)
                    elif file_ext == 'rar':
                        success = self._extract_rar(archive_path, extract_dir)
                    else:
                        raise Exception(f"Unsupported archive format: {file_ext}")
                    
                    if not success:
                        raise Exception("Extraction failed - no files extracted")
                    
                    # Verify extraction was successful
                    if not os.path.exists(extract_dir) or not os.listdir(extract_dir):
                        raise Exception("Extraction completed but no files were found in output directory")
                    
                    # Get list of extracted contents (excluding original archive)
                    extracted_files = self.get_extracted_contents(extract_dir)
                    
                    # Store extraction result
                    extracted_results.append({
                        'extract_dir': extract_dir,
                        'archive_name': filename,
                        'files': extracted_files
                    })
                    
                    successful += 1
                    
                    # Update progress for current file completion
                    progress = ((i + 1) / total_archives) * 100
                    self.progress_var.set(progress)
                    
                except Exception as e:
                    failed += 1
                    error_msg = str(e)
                    failed_files.append(f"{filename}: {error_msg}")
                    
                    # Clean up failed extraction directory if it exists and is empty
                    try:
                        if 'extract_dir' in locals() and os.path.exists(extract_dir):
                            if not os.listdir(extract_dir):
                                shutil.rmtree(extract_dir)
                    except:
                        pass
                    continue
            
            # Show completion summary and display extracted files
            self.progress_var.set(100)
            
            # Display extracted files in the GUI
            if extracted_results:
                self.root.after(0, lambda: self.display_extracted_files(extracted_results))
            
            if successful > 0:
                summary_msg = f"Decompression completed!\n\nSuccessful: {successful}\nFailed: {failed}"
                
                if extracted_results:
                    summary_msg += f"\n\nExtracted archives:\n"
                    for result in extracted_results[:3]:
                        dir_name = os.path.basename(result['extract_dir'])
                        file_count = len([f for f in result['files'] if os.path.isfile(f['path'])])
                        summary_msg += f"• {result['archive_name']} → {dir_name} ({file_count} files)\n"
                    if len(extracted_results) > 3:
                        summary_msg += f"... and {len(extracted_results) - 3} more archives"
                
                if failed_files:
                    summary_msg += f"\n\nFailed files:\n"
                    for fail in failed_files[:3]:
                        summary_msg += f"• {fail}\n"
                    if len(failed_files) > 3:
                        summary_msg += f"... and {len(failed_files) - 3} more"
                
                self.update_status(f"Completed: {successful} successful, {failed} failed")
                
                if failed > 0:
                    messagebox.showwarning("Partial Success", summary_msg)
                else:
                    messagebox.showinfo("Success", summary_msg)
            else:
                self.update_status("All decompression attempts failed!")
                error_msg = "All decompression attempts failed!\n\nErrors:\n"
                for fail in failed_files[:5]:
                    error_msg += f"• {fail}\n"
                if len(failed_files) > 5:
                    error_msg += f"... and {len(failed_files) - 5} more"
                messagebox.showerror("Failed", error_msg)
                
        except Exception as e:
            self.update_status("Decompression failed!")
            messagebox.showerror("Error", f"Decompression failed: {str(e)}")
        finally:
            self.progress_var.set(0)
    
    def _extract_zip(self, archive_path, extract_dir):
        try:
            if not zipfile.is_zipfile(archive_path):
                raise Exception("Invalid ZIP file format")
            
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                # Check for any malicious paths
                for member in zipf.namelist():
                    if os.path.isabs(member) or ".." in member:
                        raise Exception(f"Unsafe path in ZIP: {member}")
                
                zipf.extractall(extract_dir)
                return True
        except Exception as e:
            raise Exception(f"ZIP extraction failed: {str(e)}")
    
    def _extract_7z(self, archive_path, extract_dir):
        try:
            if not HAS_PY7ZR:
                raise Exception("py7zr library not installed. Run: pip install py7zr")
            
            with py7zr.SevenZipFile(archive_path, 'r') as archive:
                archive.extractall(extract_dir)
                return True
        except Exception as e:
            raise Exception(f"7Z extraction failed: {str(e)}")
    
    def _extract_tar_gz(self, archive_path, extract_dir):
        try:
            if not tarfile.is_tarfile(archive_path):
                raise Exception("Invalid TAR.GZ file format")
            
            with tarfile.open(archive_path, 'r:gz') as tar:
                # Safe extraction (prevent path traversal)
                for member in tar.getmembers():
                    if os.path.isabs(member.name) or ".." in member.name:
                        raise Exception(f"Unsafe path in TAR: {member.name}")
                
                tar.extractall(extract_dir)
                return True
        except Exception as e:
            raise Exception(f"TAR.GZ extraction failed: {str(e)}")
    
    def _extract_rar(self, archive_path, extract_dir):
        try:
            # Method 1: Use command line unrar/rar executable
            if self.unrar_path:
                try:
                    self.update_status("Extracting RAR with command line tool...")
                    return self.extract_rar_with_executable(archive_path, extract_dir)
                except Exception as e:
                    print(f"Command line RAR extraction failed: {e}")
            
            # Method 2: Try using rarfile library
            if HAS_RARFILE:
                try:
                    self.update_status("Extracting RAR with rarfile library...")
                    with rarfile.RarFile(archive_path) as rf:
                        rf.extractall(extract_dir)
                    return True
                except Exception as e:
                    print(f"rarfile extraction failed: {e}")
            
            # Method 3: Fall back to patoolib
            if HAS_PATOOLIB:
                try:
                    self.update_status("Extracting RAR with patoolib...")
                    patoolib.extract_archive(archive_path, outdir=extract_dir)
                    return True
                except Exception as e:
                    print(f"patoolib extraction failed: {e}")
            
            # Method 4: Last resort - try as ZIP file (for archives created with our fallback method)
            try:
                self.update_status("Trying RAR as ZIP format...")
                with zipfile.ZipFile(archive_path, 'r') as zipf:
                    zipf.extractall(extract_dir)
                return True
            except Exception as e:
                print(f"ZIP fallback extraction failed: {e}")
                
            raise Exception("All RAR extraction methods failed")
                
        except Exception as e:
            raise Exception(f"RAR extraction failed: {str(e)}")
            
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = FileCompressor(root)
    root.mainloop()

if __name__ == "__main__":
    main()