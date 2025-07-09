import numpy as np
import matplotlib.pyplot as plt

# Contoh aliasing pada sinusoidal
fs = 100  # Frekuensi sampling
t = np.linspace(0, 1, fs, endpoint=False)
f_high = 70  # Frekuensi di atas Nyquist (50 Hz)
f_low = 30   # Frekuensi hasil aliasing

signal_high = np.sin(2 * np.pi * f_high * t)
signal_low = np.sin(2 * np.pi * f_low * t)

plt.figure(figsize=(10, 4))
plt.plot(t, signal_high, 'r', label=f'{f_high} Hz (Asli)')
plt.plot(t, signal_low, 'b--', label=f'{f_low} Hz (Aliasing)')
plt.title(f'Aliasing: {f_high} Hz → {f_low} Hz saat f_s = {fs} Hz')
plt.legend()
plt.show()