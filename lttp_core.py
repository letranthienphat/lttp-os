import tkinter as tk
import pickle
import os

class ComputerHardwareController:
    def __init__(self):
        self.hardware_state_file = "lttp.os"
        self.load_state()

    def load_state(self):
        if os.path.exists(self.hardware_state_file):
            with open(self.hardware_state_file, "rb") as f:
                self.state = pickle.load(f)
        else:
            self.state = "Khởi động sạch"

    def turn_on_display(self):
        root = tk.Tk()
        root.title("LTTP.OS 2026 - Booted from Cloud")
        root.geometry("800x600")
        root.configure(bg="#060813")
        
        # Thêm hiệu ứng giao diện
        label = tk.Label(root, text="CHÀO MỪNG PHÁT ĐẾN VỚI LTTP.OS", 
                         font=("Segoe UI", 20, "bold"), fg="#00f0ff", bg="#060813")
        label.pack(expand=True)
        
        root.mainloop()
