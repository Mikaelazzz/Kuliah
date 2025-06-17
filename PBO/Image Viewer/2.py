import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.current_folder = ""
        self.image_files = []
        self.current_index = 0
        self.current_image = None
        
        # Supported image formats
        self.supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#8095EA', height=60)
        header_frame.pack(fill='x', padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Image Viewer", 
                              font=('Arial', 16, 'bold'), 
                              fg='white', bg='#8095EA')
        title_label.pack(pady=15)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#8095EA')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Image display area
        self.image_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=2)
        self.image_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.image_label = tk.Label(self.image_frame, text="Tidak ada gambar yang dipilih", 
                                   font=('Arial', 12), bg='white', fg='gray')
        self.image_label.pack(expand=True)
        
        # Info label
        self.info_label = tk.Label(main_frame, text="", font=('Arial', 10), 
                                  bg='#8095EA', fg='#2c3e50')
        self.info_label.pack(pady=5)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg='#8095EA')
        control_frame.pack(pady=10)
        
        # Open button
        self.open_btn = tk.Button(control_frame, text="Buka Folder", 
                                 command=self.open_folder,
                                 font=('Arial', 10, 'bold'),
                                 bg='#3B74CA', fg='white',
                                 padx=20, pady=5,
                                 cursor='hand2')
        self.open_btn.pack(side='left', padx=5)
        
        # Previous button
        self.prev_btn = tk.Button(control_frame, text="◀ Sebelumnya", 
                                 command=self.prev_image,
                                 font=('Arial', 10),
                                 bg='#95a5a6', fg='white',
                                 padx=15, pady=5,
                                 cursor='hand2',
                                 state='disabled')
        self.prev_btn.pack(side='left', padx=5)
        
        # Next button
        self.next_btn = tk.Button(control_frame, text="Selanjutnya ▶", 
                                 command=self.next_image,
                                 font=('Arial', 10),
                                 bg='#95a5a6', fg='white',
                                 padx=15, pady=5,
                                 cursor='hand2',
                                 state='disabled')
        self.next_btn.pack(side='left', padx=5)
        
        # Bind keyboard events
        self.root.bind('<Left>', lambda e: self.prev_image())
        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('<Control-o>', lambda e: self.open_folder())
        self.root.focus_set()
        
    def open_folder(self):
        folder_path = filedialog.askdirectory(title="Pilih folder yang berisi gambar")
        if folder_path:
            self.current_folder = folder_path
            self.load_images_from_folder()
            
    def load_images_from_folder(self):
        try:
            # Get all files in the folder
            all_files = os.listdir(self.current_folder)
            
            # Filter image files
            self.image_files = [f for f in all_files 
                               if f.lower().endswith(self.supported_formats)]
            
            if self.image_files:
                self.image_files.sort()  # Sort alphabetically
                self.current_index = 0
                self.display_current_image()
                self.update_buttons()
                self.update_info()
            else:
                messagebox.showinfo("No Images", "No supported image files found in the selected folder.")
                self.reset_display()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading folder: {str(e)}")
            
    def display_current_image(self):
        if not self.image_files:
            return
            
        try:
            image_path = os.path.join(self.current_folder, self.image_files[self.current_index])
            
            # Open and resize image
            pil_image = Image.open(image_path)
            
            # Calculate size to fit in display area while maintaining aspect ratio
            display_width = self.image_frame.winfo_width() - 20
            display_height = self.image_frame.winfo_height() - 20
            
            if display_width <= 1 or display_height <= 1:
                # If frame size not available yet, use default
                display_width = 760
                display_height = 400
            
            # Calculate scaling
            image_width, image_height = pil_image.size
            scale_w = display_width / image_width
            scale_h = display_height / image_height
            scale = min(scale_w, scale_h, 1)  # Don't upscale
            
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            
            # Resize image
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.current_image = ImageTk.PhotoImage(pil_image)
            
            # Update label
            self.image_label.configure(image=self.current_image, text="")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")
            
    def prev_image(self):
        if self.image_files:
            if self.current_index > 0:
                self.current_index -= 1
            else:
                # If at first image, go to last image (circular)
                self.current_index = len(self.image_files) - 1
            self.display_current_image()
            self.update_buttons()
            self.update_info()
            
    def next_image(self):
        if self.image_files:
            if self.current_index < len(self.image_files) - 1:
                self.current_index += 1
            else:
                # If at last image, go to first image (circular)
                self.current_index = 0
            self.display_current_image()
            self.update_buttons()
            self.update_info()
            
    def update_buttons(self):
        if self.image_files:
            # Always enable both buttons when there are images (circular navigation)
            self.prev_btn.configure(state='normal', bg='#3B74CA')
            self.next_btn.configure(state='normal', bg='#3B74CA')
        else:
            self.prev_btn.configure(state='disabled', bg='#95a5a6')
            self.next_btn.configure(state='disabled', bg='#95a5a6')
            
    def update_info(self):
        if self.image_files:
            current_file = self.image_files[self.current_index]
            info_text = f"Gambar {self.current_index + 1} of {len(self.image_files)}: {current_file}"
            # Add circular indicator if there are multiple images
            if len(self.image_files) > 1:
                info_text += ""
            self.info_label.configure(text=info_text)
        else:
            self.info_label.configure(text="")
            
    def reset_display(self):
        self.image_label.configure(image="", text="Tidak ada gambar yang dipilih")
        self.current_image = None
        self.image_files = []
        self.current_index = 0
        self.update_buttons()
        self.update_info()

def main():
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()