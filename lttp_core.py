import tkinter as tk
from tkinter import messagebox
import os
import shutil
import time

class LttpOSCore:
    def __init__(self):
        # Hệ thống file thực tế (thay vì file ảo cứng nhắc)
        self.root_dir = "user_data"
        if not os.path.exists(self.root_dir):
            os.makedirs(os.path.join(self.root_dir, "System_Files"))
            os.makedirs(os.path.join(self.root_dir, "My_Documents"))
        
        self.system_path = os.path.join(self.root_dir, "System_Files")

    def check_integrity(self):
        """Kiểm tra xem thư mục hệ thống có còn tồn tại không"""
        return os.path.exists(self.system_path)

    def trigger_bsod(self, root, error_msg):
        """Màn hình đen chết chóc của riêng bạn"""
        root.destroy()
        bsod = tk.Tk()
        bsod.attributes('-fullscreen', True)
        bsod.configure(bg="black")
        
        # Mô phỏng CMD lỗi
        cmd_win = tk.Label(bsod, text=f"FATAL SYSTEM ERROR:\n{error_msg}\n\nCRITICAL DIRECTORY MISSING: {self.system_path}\nRECOVERING FROM CLOUD...",
                           font=("Consolas", 14), fg="red", bg="black", justify=tk.LEFT)
        cmd_win.pack(pady=50, padx=50)
        
        bsod.after(3000, lambda: [bsod.destroy(), self.reboot_system()])
        bsod.mainloop()

    def reboot_system(self):
        # Trigger lại manager.py để tải lại hệ thống
        os.system("python manager.py")
        exit()

class LttpOSRuntime:
    def __init__(self, root, core):
        self.root = root
        self.core = core
        self.load_desktop()

    def load_desktop(self):
        # Giao diện đơn giản hiển thị thư mục
        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        btn = tk.Button(self.frame, text="XÓA THƯ MỤC HỆ THỐNG (TEST)", command=self.delete_system_folder)
        btn.pack(pady=20)
        
        self.file_list = tk.Listbox(self.frame)
        self.file_list.pack()
        self.refresh_files()

    def refresh_files(self):
        self.file_list.delete(0, tk.END)
        for f in os.listdir(self.core.root_dir):
            self.file_list.insert(tk.END, f)

    def delete_system_folder(self):
        if messagebox.askyesno("CẢNH BÁO", "Bạn chắc chắn muốn xóa thư mục hệ thống?"):
            shutil.rmtree(self.core.system_path)
            messagebox.showwarning("Cảnh báo", "Thư mục đã biến mất. Hệ thống sẽ lỗi khi bạn truy cập vào nó!")
            self.refresh_files()

    def access_system(self):
        """Giả lập một hành động truy cập hệ thống"""
        if not self.core.check_integrity():
            self.core.trigger_bsod(self.root, "EXCEPTION_ACCESS_VIOLATION_0x00001")
