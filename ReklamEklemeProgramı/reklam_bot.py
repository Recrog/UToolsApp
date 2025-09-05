import tkinter as tk
from tkinter import messagebox
import pyautogui
import time

# Ekran görüntüsü dosya adları
ADD_AD_IMG = "add_ad.png"
TIME_INPUT_IMG = "time_input.png"

# --- Yardımcı fonksiyon: bir elementi birkaç kez dene ---
def find_with_retry(img, retries=5, delay=0.5):
    for i in range(retries):
        pos = pyautogui.locateCenterOnScreen(img, confidence=0.8)
        if pos:
            return pos
        time.sleep(delay)  # tekrar denemeden önce biraz bekle
    return None

def start_process():
    try:
        total_minutes = int(entry_minutes.get())
    except ValueError:
        messagebox.showerror("Hata", "Geçerli bir sayı gir!")
        return

    messagebox.showinfo("Başlıyor", "YouTube Studio ekranını açık bırak.\n\n5 saniye içinde başlıyoruz!")
    time.sleep(5)

    for minute in range(1, total_minutes + 1):
        # Zaman kutusunu bul (retry ile)
        time_box = find_with_retry(TIME_INPUT_IMG, retries=5, delay=0.7)
        if time_box:
            pyautogui.click(time_box)
            time.sleep(0.2)
            pyautogui.typewrite(f"{minute:02d}:00")
            time.sleep(0.2)
        else:
            messagebox.showerror("Hata", f"Zaman kutusu bulunamadı (dakika {minute})!")
            return

        # Reklam ekle butonunu bul (retry ile)
        add_button = find_with_retry(ADD_AD_IMG, retries=5, delay=0.7)
        if add_button:
            pyautogui.click(add_button)
            time.sleep(0.5)
        else:
            messagebox.showerror("Hata", f"Reklam ekle butonu bulunamadı (dakika {minute})!")
            return

    messagebox.showinfo("Tamamlandı", "Tüm reklamlar yerleştirildi ✅")

# --- GUI ---
root = tk.Tk()
root.title("YouTube Reklam Otomasyonu")
root.geometry("300x150")

label = tk.Label(root, text="Video süresi (dakika):")
label.pack(pady=10)

entry_minutes = tk.Entry(root, justify="center")
entry_minutes.pack()

btn_start = tk.Button(root, text="Başlat", command=start_process, bg="green", fg="white")
btn_start.pack(pady=20)

root.mainloop()
