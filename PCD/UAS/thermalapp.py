import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

def pixel_to_temp(pixel_value, t_min=20, t_max=40):
    return t_min + (t_max - t_min) * (pixel_value / 255)

def cv2_to_tk(img_cv):
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    return ImageTk.PhotoImage(img_pil)

def cv2gray_to_tk(img_gray):
    img_pil = Image.fromarray(img_gray)
    return ImageTk.PhotoImage(img_pil)

canvas_width = 220
canvas_height = 180

root = tk.Tk()
root.title('Thermal Camera Segmentation App')
root.geometry('900x500')

opsi_var = tk.IntVar(value=1)

frame_opsi = tk.Frame(root)
frame_opsi.pack(pady=10)

rb1 = tk.Radiobutton(frame_opsi, text='1. Analisis Gambar', variable=opsi_var, value=1, font=('Arial', 12))
rb1.pack(side='left', padx=10)
rb2 = tk.Radiobutton(frame_opsi, text='2. Analisis Webcam Realtime', variable=opsi_var, value=2, font=('Arial', 12))
rb2.pack(side='left', padx=10)

frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

canvas_frame = tk.Frame(root)
canvas_frame.pack(pady=20)

canvas1 = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height, bg='gray')
canvas1.grid(row=0, column=0, padx=10)
canvas2 = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height, bg='gray')
canvas2.grid(row=0, column=1, padx=10)
canvas3 = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height, bg='gray')
canvas3.grid(row=0, column=2, padx=10)

label1 = tk.Label(canvas_frame, text='Gambar/Webcam', font=('Arial', 10))
label1.grid(row=1, column=0, pady=(5,0))
label2 = tk.Label(canvas_frame, text='Segmentasi Area Panas', font=('Arial', 10))
label2.grid(row=1, column=1, pady=(5,0))
label3 = tk.Label(canvas_frame, text='Efek Thermal (Colormap)', font=('Arial', 10))
label3.grid(row=1, column=2, pady=(5,0))

label_suhu = tk.Label(root, text='Suhu Area Panas : -', font=('Arial', 14))
label_suhu.pack(pady=10)

def segmentasi_gambar_tk(path, canvas1, canvas2, canvas3, label_suhu):
    image = cv2.imread(path)
    if image is None:
        messagebox.showerror('Error', 'Gambar tidak ditemukan.')
        return
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    threshold_value = 180
    _, hot_area = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    hot_pixels = gray[hot_area == 255]
    if hot_pixels.size > 0:
        avg_pixel = np.mean(hot_pixels)
        est_temp = pixel_to_temp(avg_pixel)
        temp_text = f"Suhu Area Panas: {est_temp:.1f}°C"
    else:
        temp_text = "Suhu Area Panas: -"

    thermal_colormap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    # Resize
    img1 = cv2.resize(image, (canvas_width, canvas_height))
    img2 = cv2.resize(hot_area, (canvas_width, canvas_height))
    img3 = cv2.resize(thermal_colormap, (canvas_width, canvas_height))
    tk_img1 = cv2_to_tk(img1)
    tk_img2 = cv2gray_to_tk(img2)
    tk_img3 = cv2_to_tk(img3)
    canvas1.img = tk_img1
    canvas2.img = tk_img2
    canvas3.img = tk_img3
    canvas1.create_image(0, 0, anchor='nw', image=tk_img1)
    canvas2.create_image(0, 0, anchor='nw', image=tk_img2)
    canvas3.create_image(0, 0, anchor='nw', image=tk_img3)
    label_suhu.config(text=temp_text)

def pilih_gambar_tk(canvas1, canvas2, canvas3, label_suhu):
    path = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg *.jpeg *.png')])
    if path:
        segmentasi_gambar_tk(path, canvas1, canvas2, canvas3, label_suhu)

cap = None
webcam_running = False
def webcam_update():
    global cap, webcam_running
    if not webcam_running:
        return
    ret, frame = cap.read()
    if not ret:
        return
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, hot_area = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    hot_pixels = gray[hot_area == 255]
    if hot_pixels.size > 0:
        avg_pixel = np.mean(hot_pixels)
        est_temp = pixel_to_temp(avg_pixel)
        temp_text = f"Suhu Area Panas: {est_temp:.1f}°C"
    else:
        temp_text = "Suhu Area Panas: -"
    thermal_colormap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    img1 = cv2.resize(frame, (canvas_width, canvas_height))
    img2 = cv2.resize(hot_area, (canvas_width, canvas_height))
    img3 = cv2.resize(thermal_colormap, (canvas_width, canvas_height))
    tk_img1 = cv2_to_tk(img1)
    tk_img2 = cv2gray_to_tk(img2)
    tk_img3 = cv2_to_tk(img3)
    canvas1.img = tk_img1
    canvas2.img = tk_img2
    canvas3.img = tk_img3
    canvas1.create_image(0, 0, anchor='nw', image=tk_img1)
    canvas2.create_image(0, 0, anchor='nw', image=tk_img2)
    canvas3.create_image(0, 0, anchor='nw', image=tk_img3)
    label_suhu.config(text=temp_text)
    root.after(30, webcam_update)

def start_webcam_tk():
    global cap, webcam_running
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror('Error', 'Webcam tidak terdeteksi.')
        return
    btn_start.config(state='disabled')
    btn_stop.config(state='normal')
    webcam_running = True
    webcam_update()

def stop_webcam_tk():
    global cap, webcam_running
    webcam_running = False
    btn_start.config(state='normal')
    btn_stop.config(state='disabled')
    if cap is not None:
        cap.release()
        cap = None

def jalankan_opsi():
    if opsi_var.get() == 1:
        stop_webcam_tk()
        pilih_gambar_tk(canvas1, canvas2, canvas3, label_suhu)
    else:
        start_webcam_tk()

frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

btn_start = tk.Button(frame_btn, text='Jalankan', font=('Arial', 12), width=12, command=jalankan_opsi)
btn_start.pack(side='left', padx=10)

btn_stop = tk.Button(frame_btn, text='Stop Webcam', font=('Arial', 12), width=12, state='disabled', command=stop_webcam_tk)
btn_stop.pack(side='left', padx=10)

root.mainloop()
