import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import tarfile
import os
from pathlib import Path
import threading
import shutil

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
        
        self.create_widgets()
        self.check_dependencies()
        
    def check_dependencies(self):
        """Check if required libraries are installed"""
        missing = []
        if not HAS_PY7ZR:
            missing.append("py7zr (for 7z files)")
        if not HAS_PATOOLIB:
            missing.append("patoolib (for RAR files)")
            
        if missing:
            msg = "Missing dependencies:\n\n" + "\n".join(missing)
            msg += "\n\nInstall with:\npip install py7zr patoolib"
            messagebox.showwarning("Dependencies Missing", msg)
        
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
                                   values=["zip", "7z", "tar.gz"],
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
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0
            
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def get_archive_extension(self, file_path):
        """Get the proper archive extension"""
        file_path_lower = file_path.lower()
        if file_path_lower.endswith('.tar.gz'):
            return 'tar.gz'
        elif file_path_lower.endswith('.tgz'):
            return 'tar.gz'
        else:
            return Path(file_path).suffix[1:]  # Remove the dot
    
    def display_extracted_files(self, extracted_results):
        """Display extracted files in the text widget"""
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
        """Get only the extracted contents, excluding the original archive file"""
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
            
            self.progress_var.set(100)
            self.update_status(f"Compression completed: {os.path.basename(archive_path)}")
            messagebox.showinfo("Success", f"Files compressed successfully!\nSaved as: {archive_path}")
            
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
                    
                    # Create unique extraction directory
                    base_extract_dir = f"Extracted_{archive_name}"
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
        """Extract ZIP files"""
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
        """Extract 7Z files"""
        try:
            if not HAS_PY7ZR:
                raise Exception("py7zr library not installed. Run: pip install py7zr")
            
            with py7zr.SevenZipFile(archive_path, 'r') as archive:
                archive.extractall(extract_dir)
                return True
        except Exception as e:
            raise Exception(f"7Z extraction failed: {str(e)}")
    
    def _extract_tar_gz(self, archive_path, extract_dir):
        """Extract TAR.GZ files"""
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
        """Extract RAR files"""
        try:
            if not HAS_PATOOLIB:
                raise Exception("patoolib library not installed. Run: pip install patoolib")
            
            patoolib.extract_archive(archive_path, outdir=extract_dir)
            return True
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