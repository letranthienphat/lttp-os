# =====================================================================
# FILE: lttp_core.py (LTTP.OS WIN11 CLOUD - VERSION HIGH INTEGRATED)
# TÍNH NĂNG: ĐA NHIỆM, VFS MÃ HÓA, MERCURY SECURE BROWSER, DEFENDER, HOT UPDATE
# =====================================================================
import os
import sys
import time
import json
import base64
import hashlib
import threading
import uuid
import random
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, scrolledtext

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# =====================================================================
# 1. HỆ THỐNG QUẢN LÝ QUY TRÌNH DỮ LIỆU TẬP TRUNG & PHÂN TẦNG VFS MÃ HÓA
# =====================================================================
class LTPOperatingSystem:
    def __init__(self):
        self.os_name = "LTTP.OS Win11 Cloud Ultimate"
        self.version = "2026.60.0"
        self.local_data_path = "data.json" 
        self.current_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.path_mismatch = False 
        
        # Cấu hình người dùng hệ thống mặc định
        self.user_config = {
            "is_new_user": True,
            "logged_in_user": None,
            "security_password": None,     
            "saved_path": None,            
            "device_id": str(uuid.uuid4())[:8].upper(),
            "theme_color": "Cyan",         
            "font_size_offset": 0,
            "grid_lines_visible": True,
            "wallpaper_path": "Default",
            "taskbar_alignment": "Center",
            "temp_warning_limit": 75,       
            "temp_cutoff_limit": 90          
        }
        
        # Hệ thống tệp tin ảo (Virtual File System - VFS) ban đầu của Phát
        self.virtual_files = {
            "lttp_readme.txt": "Chào mừng bạn đến với hệ điều hành LTTP.OS Cloud Ultimate mượt mà!".encode('utf-8'),
            "Bai_Tap_Toan_7.txt": "Bài 1: Tính diện tích hình lăng trụ đứng tam giác.\nBài 2: Tính chất số hữu tỉ.".encode('utf-8'),
            "Nhat_Ky_Long_Hai.txt": "Kỷ niệm chuyến đi chơi mùng 3 mùng 4 Tết âm lịch vô cùng vui vẻ cùng gia đình.".encode('utf-8'),
            "Am_Thanh_TV.mp3": "Mô phỏng luồng phát tín hiệu âm thanh không dây từ Tivi sang tai nghe của Ba.".encode('utf-8'),
            "he_thong.sys": "INTEGRITY_CHECK_PASSED_CORE_VALID_100".encode('utf-8')
        }
        
        # Cơ sở dữ liệu chữ ký mã độc của LTTP Defender
        self.signatures = {
            "WannaCry": "A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3",
            "Trojan.Spyware": "5D41402ABC4B2A76B9719D911017C592"
        }
        self.load_unified_data_file()

    def load_unified_data_file(self):
        """Đọc và giải mã Base64 hệ thống tệp tin ảo từ dữ liệu cấu hình data.json"""
        if os.path.exists(self.local_data_path):
            try:
                with open(self.local_data_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.user_config.update(saved.get("config", {}))
                    if "virtual_files" in saved:
                        for k, v in saved["virtual_files"].items():
                            self.virtual_files[k] = base64.b64decode(v.encode('utf-8'))
                            
                if self.user_config.get("logged_in_user") is not None:
                    self.user_config["is_new_user"] = False
                    saved_p = self.user_config.get("saved_path")
                    if saved_p != self.current_path:
                        self.path_mismatch = True
                else:
                    self.user_config["is_new_user"] = True
            except: pass

    def save_local_state_file(self):
        """Mã hóa toàn bộ tệp ảo sang dạng Base64 và nén chặt lưu vào ổ đĩa máy thật"""
        try:
            converted_files = {}
            for k, v in self.virtual_files.items():
                converted_files[k] = base64.b64encode(v).decode('utf-8')
            to_save = {"config": self.user_config, "virtual_files": converted_files, "signatures": self.signatures}
            with open(self.local_data_path, "w", encoding="utf-8") as f:
                json.dump(to_save, f, indent=4)
        except: pass

# =====================================================================
# 2. GIAO DIỆN ĐỒ HỌA ĐA NHIỆM & ENGINE ĐIỀU HÀNH MÁY ẢO
# =====================================================================
class LttpOSRuntime:
    def __init__(self, root, os_core_instance, save_callback):
        self.root = root
        self.os_core = os_core_instance
        self.save_hardware_state = save_callback
        
        # Trạng thái giả lập phần cứng thời gian thực
        self.hardware = {"cpu_temp": 46.2, "ram_usage": 1.45, "fan_rpm": 2100, "is_bsod": False}
        self.running_processes = ["System Kernel", "Desktop Shell", "Hardware Monitor Engine"]
        
        self.apply_fullscreen_logic()
        self.refresh_ui_colors()
        
        # Kiểm tra điều kiện bảo mật trước khi vào Desktop
        if self.os_core.user_config.get("is_new_user", True):
            self.show_registration_wizard()
        elif self.os_core.path_mismatch:
            self.show_security_path_reauth_screen()
        else:
            self.load_desktop_interface()
            
            # 🚀 TRƯỜNG HỢP 1: TỰ ĐỘNG QUÉT UPDATE SAU KHI KHỞI ĐỘNG VÀO DESKTOP THÀNH CÔNG 1.5 GIÂY
            if "CLOUD_UPDATER" in globals():
                self.root.after(1500, lambda: globals()["CLOUD_UPDATER"](manual=False, root_win=self.root))

        self.start_hardware_background_simulation()

    def apply_fullscreen_logic(self):
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))

    def refresh_ui_colors(self):
        """Hệ thống tùy biến bảng màu Neon đặc trưng của Phát"""
        accent = "#00f0ff" # Cyan mặc định
        c_name = self.os_core.user_config.get("theme_color", "Cyan")
        if c_name == "Red": accent = "#ff0055"
        elif c_name == "Green": accent = "#00ff66"
        elif c_name == "Purple": accent = "#bd00ff"
        
        self.ui = {
            "bg": "#060813", "taskbar": "#0f1224", "text": "#f1f5f9",
            "accent": accent, "card": "#111424", "danger": "#ff0055", "success": "#00ff66"
        }
        
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook', background=self.ui["bg"], borderwidth=0)
        self.style.configure('TNotebook.Tab', background="#161b33", foreground=self.ui["text"], padding=[12, 5])
        self.style.map('TNotebook.Tab', background=[('selected', self.ui["card"])], foreground=[('selected', self.ui["accent"])])

    def bind_hover_animation(self, widget, hover_bg, normal_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    def run_smooth_progress_bar(self, pbar, current_val, target_val, speed=5, callback=None):
        if current_val < target_val:
            current_val += speed
            if current_val > target_val: current_val = target_val
            pbar['value'] = current_val
            self.root.after(15, lambda: self.run_smooth_progress_bar(pbar, current_val, target_val, speed, callback))
        elif callback:
            callback()

    def show_registration_wizard(self):
        """Màn hình thiết lập Khóa bảo mật tối cao lần đầu"""
        self.auth_container = tk.Frame(self.root, bg=self.ui["bg"])
        self.auth_container.pack(fill=tk.BOTH, expand=True)
        panel = tk.Frame(self.auth_container, bg=self.ui["card"], bd=1, relief=tk.SOLID, highlightthickness=1, highlightbackground=self.ui["accent"])
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=550, height=420)
        
        tk.Label(panel, text="✨ THIẾT LẬP LTTP.OS KHỞI CHẠY LẦN ĐẦU ✨", font=("Segoe UI", 12, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=20)
        lbl_info = "Chào mừng Phát đến với nhân lõi hệ điều hành bảo mật!\nVui lòng tạo mật mã quản trị tối cao để kích hoạt khóa mã hóa hệ thống tệp tin:"
        tk.Label(panel, text=lbl_info, font=("Segoe UI", 9), fg=self.ui["text"], bg=self.ui["card"], justify=tk.CENTER).pack(pady=5)
        
        tk.Label(panel, text="Tên Quản Trị Viên (Username):", fg=self.ui["accent"], bg=self.ui["card"], font=("Segoe UI", 9, "bold")).pack(pady=(15, 2))
        ent_user = tk.Entry(panel, font=("Segoe UI", 10), width=30, bg="#0d1117", fg="white", insertbackground="white", justify=tk.CENTER)
        ent_user.pack()
        ent_user.insert(0, "LeTranThienPhat")
        
        tk.Label(panel, text="Mật Khẩu Hệ Thống (Security Password):", fg=self.ui["accent"], bg=self.ui["card"], font=("Segoe UI", 9, "bold")).pack(pady=(15, 2))
        ent_pass = tk.Entry(panel, font=("Segoe UI", 10), width=30, bg="#0d1117", fg="white", show="*", insertbackground="white", justify=tk.CENTER)
        ent_pass.pack()
        
        def thuc_hien_dang_ky():
            username = ent_user.get().strip()
            password = ent_pass.get().strip()
            if not username or not password:
                messagebox.showwarning("Lỗi Thiết Lập", "Không được bỏ trống thông tin an ninh tài khoản!")
                return
            self.os_core.user_config["is_new_user"] = False
            self.os_core.user_config["logged_in_user"] = username
            self.os_core.user_config["security_password"] = password
            self.os_core.user_config["saved_path"] = self.os_core.current_path
            self.os_core.save_local_state_file()
            messagebox.showinfo("Kích Hoạt", f"✅ Tài khoản quản trị cấp cao '{username}' khởi tạo thành công!")
            self.auth_container.destroy()
            self.load_desktop_interface()

            if "CLOUD_UPDATER" in globals():
                globals()["CLOUD_UPDATER"](manual=False, root_win=self.root)

        btn_register = tk.Button(panel, text="🔐 KÍCH HOẠT HỆ THỐNG & KHỞI ĐỘNG DESKTOP", bg=self.ui["accent"], fg="black", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=20, pady=8, command=thuc_hien_dang_ky)
        btn_register.pack(pady=30)
        self.bind_hover_animation(btn_register, "#ffffff", self.ui["accent"])

    def show_security_path_reauth_screen(self):
        """Lớp lá chắn chống đánh cắp dữ liệu khi di chuyển file bừa bãi"""
        self.auth_container = tk.Frame(self.root, bg=self.ui["bg"])
        self.auth_container.pack(fill=tk.BOTH, expand=True)
        panel = tk.Frame(self.auth_container, bg="#120811", bd=1, relief=tk.SOLID, highlightthickness=1, highlightbackground=self.ui["danger"])
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=640, height=450)
        
        tk.Label(panel, text="🚨 CẢNH BÁO: KHÔNG GIAN THỰC THI BỊ THAY ĐỔI 🚨", font=("Segoe UI", 11, "bold"), fg=self.ui["danger"], bg="#120811").pack(pady=15)
        warn_txt = (
            f"Lá chắn an ninh phát hiện tệp lõi LTTP.OS bị sao chép hoặc di chuyển thư mục trái phép!\n\n"
            f"📍 Thư mục đăng ký gốc:\n -> {self.os_core.user_config.get('saved_path')}\n\n"
            f"⚡ Vị trí thực thi hiện tại:\n -> {self.os_core.current_path}\n\n"
            f"Vui lòng xác minh mật mã tài khoản [{self.os_core.user_config.get('logged_in_user')}] để tái cấp quyền:"
        )
        tk.Label(panel, text=warn_txt, font=("Consolas", 9), fg="#e2e8f0", bg="#120811", justify=tk.LEFT, padx=20).pack(pady=5)
        
        tk.Label(panel, text="Nhập Mật Khẩu Xác Minh:", fg=self.ui["danger"], bg="#120811", font=("Segoe UI", 9, "bold")).pack(pady=(15, 2))
        ent_pass = tk.Entry(panel, font=("Segoe UI", 10), width=30, bg="#0d1117", fg="white", show="*", insertbackground="white", justify=tk.CENTER)
        ent_pass.pack()
        
        def thuc_hien_xac_thuc_lai():
            if ent_pass.get().strip() == self.os_core.user_config.get("security_password"):
                self.os_core.user_config["saved_path"] = self.os_core.current_path
                self.os_core.path_mismatch = False
                self.os_core.save_local_state_file()
                messagebox.showinfo("Xác Thực", "✅ Đồng bộ vị trí thư mục thực thi mới thành công!")
                self.auth_container.destroy()
                self.load_desktop_interface()
                
                if "CLOUD_UPDATER" in globals():
                    globals()["CLOUD_UPDATER"](manual=False, root_win=self.root)
            else:
                messagebox.showerror("An Ninh Từ Chối", "❌ Mật khẩu hệ thống hoàn toàn sai lệch!")

        btn_auth = tk.Button(panel, text="🔓 CẬP NHẬT ĐƯỜNG DẪN & REBOOT MÁY ÀO", bg=self.ui["danger"], fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=15, pady=8, command=thuc_hien_xac_thuc_lai)
        btn_auth.pack(pady=25)
        self.bind_hover_animation(btn_auth, "#ff4d4d", self.ui["danger"])

    def load_desktop_interface(self):
        """Tải không gian làm việc Desktop chuẩn Win11"""
        self.desktop_canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.ui["bg"])
        self.desktop_canvas.pack(fill=tk.BOTH, expand=True)
        self.apply_wallpaper_engine(self.desktop_canvas)
        
        # Kiến trúc thanh Taskbar bên dưới màn hình
        align = self.os_core.user_config.get("taskbar_alignment", "Center")
        self.taskbar = tk.Frame(self.desktop_canvas, bg=self.ui["taskbar"], height=50)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X, padx=30, pady=15)
        
        dock = tk.Frame(self.taskbar, bg=self.ui["taskbar"])
        if align == "Center": dock.pack(expand=True, fill=tk.Y)
        else: dock.pack(side=tk.LEFT, padx=15, fill=tk.Y)
            
        self.start_btn = tk.Button(dock, text="❖", bg=self.ui["accent"], fg="black", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, width=4, command=self.trigger_start_menu)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        apps_bar = [
            ("📁 Explorer", self.open_file_explorer_app),
            ("🛡️ Defender", self.open_defender_security_app),
            ("🌐 Mercury", self.open_mercury_secure_browser),
            ("📊 TaskMgr", self.open_task_manager_app),
            ("⚙️ Cài đặt", self.open_advanced_settings_app)
        ]
        for name, cmd in apps_bar:
            b = tk.Button(dock, text=name, bg="#1e293b", fg="white", font=("Segoe UI", 9), relief=tk.FLAT, command=cmd)
            b.pack(side=tk.LEFT, padx=3, pady=5)
            self.bind_hover_animation(b, self.ui["accent"], "#1e293b")
            
        self.hw_lbl = tk.Label(self.taskbar, text="", font=("Consolas", 9, "bold"), fg=self.ui["accent"], bg=self.ui["taskbar"], justify=tk.RIGHT)
        self.hw_lbl.pack(side=tk.RIGHT, padx=15)
        
        self.app_icon_grid = tk.Frame(self.desktop_canvas, bg="")
        self.draw_desktop_icons()

    def apply_wallpaper_engine(self, container):
        w_path = self.os_core.user_config.get("wallpaper_path", "Default")
        if w_path != "Default" and os.path.exists(w_path) and Image is not None:
            try:
                img = Image.open(w_path)
                sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
                img = img.resize((sw, sh), Image.Resampling.LANCZOS)
                self.root.bg_img_cached = ImageTk.PhotoImage(img)
                bg_lbl = tk.Label(container, image=self.root.bg_img_cached)
                bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
            except: pass

    def draw_desktop_icons(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        if self.os_core.user_config.get("grid_lines_visible", True):
            for i in range(0, w, 100): self.desktop_canvas.create_line(i, 0, i, h, fill="#0f1428", width=1)
            for j in range(0, h, 100): self.desktop_canvas.create_line(0, j, w, j, fill="#0f1428", width=1)
            
        self.desktop_canvas.create_window((50, 50), window=self.app_icon_grid, anchor="nw")
        for widget in self.app_icon_grid.winfo_children(): widget.destroy()
        self.app_icon_grid.config(bg="")
        
        f_size = 9 + self.os_core.user_config["font_size_offset"]
        apps_icons = [
            ("📁\nQuản Lý File", self.open_file_explorer_app),
            ("🛡️\nLTTP Defender", self.open_defender_security_app),
            ("🌐\nMercury Browser", self.open_mercury_secure_browser),
            ("📊\nTask Manager", self.open_task_manager_app),
            ("⚙️\nCài Đặt Hệ Thống", self.open_advanced_settings_app)
        ]
        for txt, act in apps_icons:
            btn = tk.Button(self.app_icon_grid, text=txt, font=("Segoe UI", f_size, "bold"), fg=self.ui["text"], bg="#11152c", 
                            relief=tk.FLAT, bd=0, width=13, height=4, highlightthickness=1, highlightbackground="#22294f", command=act)
            btn.pack(pady=10, side=tk.TOP)
            self.bind_hover_animation(btn, self.ui["accent"], "#11152c")

    def trigger_start_menu(self):
        user_c = self.os_core.user_config.get("logged_in_user", "Admin")
        messagebox.showinfo("LTTP Start Menu", f"🚀 {self.os_core.os_name}\n👤 Quản trị viên: {user_c}\n⚡ Kernel Build: {self.os_core.version}\n🔒 Device ID: {self.os_core.user_config['device_id']}")

    def check_system_integrity_or_crash(self):
        if "he_thong.sys" not in self.os_core.virtual_files:
            if not self.hardware["is_bsod"]:
                self.trigger_delayed_black_screen_of_death("CRITICAL_PROCESS_DIED: Missing 'he_thong.sys'. Integrity compromised.")
                return False
        return True

    def start_hardware_background_simulation(self):
        """Luồng ngầm quét và tính toán nhiệt độ, vòng quay quạt tản nhiệt"""
        if self.hardware["is_bsod"]: return
        self.hardware["cpu_temp"] += random.uniform(-1.2, 1.8)
        if self.hardware["cpu_temp"] < 42: self.hardware["cpu_temp"] = 43.5
        self.hardware["fan_rpm"] = int(self.hardware["cpu_temp"] * 48)
        self.hardware["ram_usage"] = round(1.4 + random.uniform(0.02, 0.21) + (0.15 * len(self.running_processes)), 2)
        
        cutoff = self.os_core.user_config.get("temp_cutoff_limit", 90)
        warning = self.os_core.user_config.get("temp_warning_limit", 75)
        
        if self.hardware["cpu_temp"] >= cutoff:
            self.trigger_delayed_black_screen_of_death(f"HARDWARE_OVERHEAT: CPU Temp reached critical threshold ({round(self.hardware['cpu_temp'],1)}°C).")
            return
            
        status_text = f"🔥 CPU: {round(self.hardware['cpu_temp'], 1)}°C | 🌀 Quạt: {self.hardware['fan_rpm']} RPM\n💾 RAM: {self.hardware['ram_usage']} GB / 8.0 GB"
        if self.hardware["cpu_temp"] >= warning:
            status_text += " ⚠️ QUÁ NHIỆT!"
            if self.hw_lbl.winfo_exists(): self.hw_lbl.config(fg=self.ui["danger"])
        else:
            if self.hw_lbl.winfo_exists(): self.hw_lbl.config(fg=self.ui["accent"])
        if self.hw_lbl.winfo_exists(): self.hw_lbl.config(text=status_text)
        self.root.after(2000, self.start_hardware_background_simulation)

    def trigger_delayed_black_screen_of_death(self, error_msg):
        """Màn hình đen chết chóc bảo vệ phần cứng máy tính thật của Phát"""
        self.hardware["is_bsod"] = True
        for w in self.root.winfo_children(): w.destroy()
        self.root.configure(bg="black")
        bsod_frame = tk.Frame(self.root, bg="black")
        bsod_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(bsod_frame, text="▪️ SYSTEM ERROR - BLACK SCREEN OF DEATH ▪️", font=("Consolas", 14, "bold"), fg="#ff0055", bg="black").pack(pady=20)
        tk.Label(bsod_frame, text=f"Mã Lỗi: {error_msg}\n\nHệ thống tạm thời đóng băng để ngăn chặn hư hỏng phần cứng phần cứng.", font=("Consolas", 10), fg="white", bg="black", justify=tk.CENTER).pack(pady=10)
        
        def auto_repair():
            self.os_core.virtual_files["he_thong.sys"] = "INTEGRITY_CHECK_PASSED_CORE_VALID_100".encode('utf-8')
            self.os_core.save_local_state_file()
            messagebox.showinfo("Trung Tâm Cứu Hộ", "🔧 Khôi phục tệp lõi 'he_thong.sys' thành công! Đang tái khởi động...")
            self.hardware["is_bsod"] = False
            bsod_frame.destroy()
            self.__init__(self.root, self.os_core, self.save_hardware_state)

        tk.Button(bsod_frame, text="🛠️ KÍCH HOẠT AUTO REPAIR", font=("Segoe UI", 9, "bold"), bg="#11152c", fg="#00ff66", relief=tk.SOLID, padx=10, pady=5, command=auto_repair).pack(pady=35)

    # =====================================================================
    # 3. KHO ỨNG DỤNG HỆ THỐNG FULL TÍNH NĂNG CHÍNH THỨC
    # =====================================================================
    
    # 📁 ỨNG DỤNG 1: QUẢN LÝ TỆP TIN ẢO VFS EXPLORER
    def open_file_explorer_app(self):
        if not self.check_system_integrity_or_crash(): return
        if "Explorer.exe" not in self.running_processes: self.running_processes.append("Explorer.exe")
        win = tk.Toplevel(self.root)
        win.title("File Explorer - Hệ Thống VFS")
        win.geometry("640x440")
        win.configure(bg=self.ui["card"])
        
        listbox = tk.Listbox(win, bg="#0d1117", fg="white", font=("Consolas", 10), selectbackground=self.ui["accent"], selectforeground="black")
        listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def reload_files():
            listbox.delete(0, tk.END)
            for f_name in self.os_core.virtual_files.keys():
                listbox.insert(tk.END, f" 📄 {f_name.ljust(25)} (Kích thước: {len(self.os_core.virtual_files[f_name])} bytes)")
        reload_files()
        
        def doc_file():
            try:
                sel = listbox.get(listbox.curselection()).split()[1].strip()
                data = self.os_core.virtual_files[sel]
                view = tk.Toplevel(win)
                view.title(f"Đọc: {sel}")
                view.geometry("450x320")
                txt = scrolledtext.ScrolledText(view, bg="#0d1117", fg="white", font=("Consolas", 10))
                txt.pack(fill=tk.BOTH, expand=True)
                txt.insert(tk.END, data.decode('utf-8', errors='ignore'))
            except: pass

        def tao_file_moi():
            f_name = filedialog.askstring("Tạo Tệp Tin", "Nhập tên file ảo mới (ví dụ: code.py):", parent=win)
            if f_name:
                self.os_core.virtual_files[f_name] = "Mã nguồn ảo của Phát.".encode('utf-8')
                self.os_core.save_local_state_file()
                reload_files()

        def xoa_file():
            try:
                sel = listbox.get(listbox.curselection()).split()[1].strip()
                if sel == "he_thong.sys":
                    if not messagebox.askyesno("Nguy Hiểm", "Xóa file hệ thống này có thể làm sập hệ điều hành! Phát có chắc chắn không?"): return
                del self.os_core.virtual_files[sel]
                self.os_core.save_local_state_file()
                reload_files()
                self.check_system_integrity_or_crash()
            except: pass

        bf = tk.Frame(win, bg=self.ui["card"])
        bf.pack(fill=tk.X, pady=10, padx=20)
        for t, c in [("📖 Xem Tệp", doc_file), ("➕ Tạo File Ảo", tao_file_moi), ("❌ Xóa File", xoa_file)]:
            b = tk.Button(bf, text=t, font=("Segoe UI", 9, "bold"), fg="white", bg="#1e293b", relief=tk.FLAT, command=c)
            b.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)
            self.bind_hover_animation(b, self.ui["accent"], "#1e293b")
        win.protocol("WM_DELETE_WINDOW", lambda: [self.running_processes.remove("Explorer.exe") if "Explorer.exe" in self.running_processes else None, win.destroy()])

    # 🛡️ ỨNG DỤNG 2: TRUNG TÂM DIỆT VIRUS LTTP DEFENDER PRO
    def open_defender_security_app(self):
        if not self.check_system_integrity_or_crash(): return
        if "Defender.exe" not in self.running_processes: self.running_processes.append("Defender.exe")
        win = tk.Toplevel(self.root)
        win.title("LTTP Defender Engine Pro")
        win.geometry("580x420")
        win.configure(bg=self.ui["card"])
        
        p_bar = ttk.Progressbar(win, orient=tk.HORIZONTAL, length=450, mode='determinate')
        p_bar.pack(pady=15)
        log = scrolledtext.ScrolledText(win, bg="#070a14", fg="#00ff66", font=("Consolas", 9), height=14)
        log.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        def run_scan():
            log.delete("1.0", tk.END)
            log.insert(tk.END, "⚙️ Đang kích hoạt lõi quét LTTP Defender Pro...\n")
            log.insert(tk.END, f"🔍 Đang rà soát tệp phân vùng ảo: {len(self.os_core.virtual_files)} tệp tin...\n")
            
            def hoan_tat(): 
                found_virus = False
                for f_name, f_data in self.os_core.virtual_files.items():
                    content_hash = hashlib.md5(f_data).hexdigest().upper()
                    log.insert(tk.END, f" -> Đang quét {f_name}... OK\n")
                    # Giả lập phát hiện mã độc bằng hash
                    if "virus" in f_name.lower():
                        found_virus = True
                        log.insert(tk.END, f"🚨 PHÁT HIỆN MÃ ĐỘC TRONG FILE {f_name}!\n", "danger")
                if not found_virus:
                    log.insert(tk.END, "\n✅ KẾT QUẢ QUÉT: Hệ thống sạch 100%. An toàn tuyệt đối.\n")
                    
            self.run_smooth_progress_bar(p_bar, 0, 100, speed=10, callback=hoan_tat)
            
        tk.Button(win, text="🚀 BẮT ĐẦU QUÉT HỆ THỐNG", font=("Segoe UI", 9, "bold"), bg=self.ui["accent"], fg="black", padx=10, command=run_scan).pack(pady=10)
        win.protocol("WM_DELETE_WINDOW", lambda: [self.running_processes.remove("Defender.exe") if "Defender.exe" in self.running_processes else None, win.destroy()])

    # 🌐 ỨNG DỤNG 3: TRÌNH DUYỆT BẢO MẬT ĐA TAB MERCURY SECURE BROWSER
    def open_mercury_secure_browser(self):
        if not self.check_system_integrity_or_crash(): return
        if "MercuryBrowser.exe" not in self.running_processes: self.running_processes.append("MercuryBrowser.exe")
        win = tk.Toplevel(self.root)
        win.title("Mercury Secure Browser v4.0")
        win.geometry("750x500")
        win.configure(bg=self.ui["bg"])
        
        # Thanh địa chỉ và nút Tab mới
        nav_frame = tk.Frame(win, bg=self.ui["taskbar"])
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ent_url = tk.Entry(nav_frame, font=("Segoe UI", 10), bg="#0d1117", fg="white", insertbackground="white")
        ent_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        ent_url.insert(0, "https://github.com/letranthienphat")
        
        nb_browser = ttk.Notebook(win)
        nb_browser.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def navigate_url():
            url = ent_url.get().strip()
            current_tab = nb_browser.nametowidget(nb_browser.select())
            for child in current_tab.winfo_children(): child.destroy()
            
            badge_frame = tk.Frame(current_tab, bg="#0d1117")
            badge_frame.pack(fill=tk.X)
            tk.Label(badge_frame, text="🔒 MERCURY SHIELD SECURE", font=("Segoe UI", 8, "bold"), fg="#00ff66", bg="#0d1117").pack(side=tk.LEFT, padx=10, pady=2)
            
            content_txt = scrolledtext.ScrolledText(current_tab, bg="#0d1117", fg="white", font=("Consolas", 10))
            content_txt.pack(fill=tk.BOTH, expand=True)
            
            content_txt.insert(tk.END, f"🌐 ĐANG TẢI DỮ LIỆU TỪ: {url}...\n\n")
            if "github.com/letranthienphat" in url.lower():
                content_txt.insert(tk.END, "📂 KHO LƯU TRỮ CHÍNH THỨC CỦA PHÁT:\n")
                content_txt.insert(tk.END, " -> Repository: lttp-os [Mã nguồn chính thức LTTP.OS]\n")
                content_txt.insert(tk.END, " -> File 1: manager.py (Trình Bootloader RAM)\n")
                content_txt.insert(tk.END, " -> File 2: lttp_core.py (Nhân Hệ Điều Hành)\n\n")
                content_txt.insert(tk.END, "💎 Trạng thái liên kết: Kết nối đám mây an toàn định danh 100%.")
            else:
                content_txt.insert(tk.END, f"Mô phỏng nội dung trang web bảo mật kết xuất thành công.\nThiết lập Sandbox cô lập mã độc bảo vệ máy tính thành công.")
                
        def open_new_tab(title="Tab Mới"):
            tab = tk.Frame(nb_browser, bg="#0d1117")
            nb_browser.add(tab, text=f" {title} ")
            nb_browser.select(tab)
            tk.Label(tab, text="MERCURY SECURE ENGINE\nNhập URL và nhấn 'Duyệt Web' để lướt Web an toàn.", font=("Segoe UI", 10), fg="#64748b", bg="#0d1117").pack(expand=True)
            
        btn_go = tk.Button(nav_frame, text="🚀 Duyệt Web", bg=self.ui["accent"], fg="black", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, command=navigate_url)
        btn_go.pack(side=tk.LEFT, padx=3)
        
        btn_add_tab = tk.Button(nav_frame, text="➕ Tab Mới", bg="#1e293b", fg="white", font=("Segoe UI", 9), relief=tk.FLAT, command=lambda: open_new_tab())
        btn_add_tab.pack(side=tk.LEFT, padx=3)
        
        open_new_tab("GitHub LTTPhat")
        navigate_url()
        win.protocol("WM_DELETE_WINDOW", lambda: [self.running_processes.remove("MercuryBrowser.exe") if "MercuryBrowser.exe" in self.running_processes else None, win.destroy()])

    # 📊 ỨNG DỤNG 4: TRÌNH QUẢN LÝ TÁC VỤ TASK MANAGER
    def open_task_manager_app(self):
        if not self.check_system_integrity_or_crash(): return
        win = tk.Toplevel(self.root)
        win.title("Task Manager - Trình Quản Lý Tác Vụ")
        win.geometry("500x380")
        win.configure(bg=self.ui["card"])
        
        tk.Label(win, text="Danh Sách Tiến Trình Hệ Thống Đang Chạy:", font=("Segoe UI", 10, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(anchor="w", padx=20, pady=10)
        
        t_box = tk.Listbox(win, bg="#0d1117", fg="white", font=("Consolas", 10), selectbackground=self.ui["danger"])
        t_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        def reload_proc():
            t_box.delete(0, tk.END)
            for p in self.running_processes:
                t_box.insert(tk.END, f" 🟢 {p.ljust(25)} [PID: {random.randint(1000,9999)}] - Running")
        reload_proc()
        
        def kill_proc():
            try:
                sel = t_box.get(t_box.curselection()).split()[1].strip()
                if sel in ["System", "Desktop", "Hardware"]:
                    messagebox.showwarning("Từ Chối", "Đây là tiến trình Core tối cao, không thể kết thúc!")
                    return
                # Giả lập kill bằng cách tắt cửa sổ có tiêu đề chứa tiến trình đó
                for w in self.root.winfo_children():
                    if isinstance(w, tk.Toplevel) and sel.replace(".exe","") in w.title():
                        w.destroy()
                if sel in self.running_processes:
                    self.running_processes.remove(sel)
                reload_proc()
            except: pass

        tk.Button(win, text="❌ End Task (Kết Thúc Tác Vụ)", font=("Segoe UI", 9, "bold"), bg=self.ui["danger"], fg="white", relief=tk.FLAT, command=kill_proc).pack(pady=15)

    # ⚙️ ỨNG DỤNG 5: CÀI ĐẶT HỆ THỐNG CAO CẤP (TÍNH NĂNG UPDATE CHÈN TẠI ĐÂY)
    def open_advanced_settings_app(self):
        if not self.check_system_integrity_or_crash(): return
        if "Settings.exe" not in self.running_processes: self.running_processes.append("Settings.exe")
        win = tk.Toplevel(self.root)
        win.title("Cài đặt Hệ Thống")
        win.geometry("560x450")
        win.configure(bg=self.ui["card"])
        
        nb = ttk.Notebook(win)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # TAB 1: Cá nhân hóa phong cách hình ảnh
        t_ui = tk.Frame(nb, bg=self.ui["card"])
        nb.add(t_ui, text="  🎨 Cá Nhân Hóa  ")
        tk.Label(t_ui, text="Chủ đề màu sắc Neon đặc trưng:", fg="white", bg=self.ui["card"]).pack(pady=10)
        cb_color = ttk.Combobox(t_ui, values=["Cyan", "Red", "Green", "Purple"], state="readonly")
        cb_color.set(self.os_core.user_config.get("theme_color", "Cyan"))
        cb_color.pack()
        
        # TAB 2: Ràng buộc ngưỡng cảnh báo phần cứng
        t_hw = tk.Frame(nb, bg=self.ui["card"])
        nb.add(t_hw, text="  ⚙️ Phần Cứng  ")
        tk.Label(t_hw, text="Ngưỡng Cảnh Báo Quá Nhiệt CPU (°C):", fg="white", bg=self.ui["card"]).pack(pady=10)
        scale_warn = tk.Scale(t_hw, from_=55, to=80, orient=tk.HORIZONTAL, bg=self.ui["card"], fg="white", highlightthickness=0)
        scale_warn.set(self.os_core.user_config.get("temp_warning_limit", 75))
        scale_warn.pack(fill=tk.X, padx=40)

        # 🌐 TAB 3: TRƯỜNG HỢP 2 - KIỂM TRA & NÂNG CẤP HỆ THỐNG CLOUD GITHUB THỦ CÔNG
        t_sys = tk.Frame(nb, bg=self.ui["card"])
        nb.add(t_sys, text="  🌐 Hệ Thống Cloud  ")
        
        tk.Label(t_sys, text=f"📦 Hệ Điều Hành: {self.os_core.os_name}", fg="white", bg=self.ui["card"], font=("Segoe UI", 10, "bold")).pack(pady=(25, 5))
        tk.Label(t_sys, text=f"🏷️ Phiên Bản Hiện Tại: v{self.os_core.version}", fg=self.ui["accent"], bg=self.ui["card"], font=("Consolas", 10)).pack(pady=5)
        tk.Label(t_sys, text="Kênh phân phối: GitHub Main Branch Production Secure Link", fg="#64748b", bg=self.ui["card"], font=("Segoe UI", 9)).pack(pady=5)
        
        def kick_hoat_manual_update():
            if "CLOUD_UPDATER" in globals():
                globals()["CLOUD_UPDATER"](manual=True, root_win=self.root)
            else:
                messagebox.showerror("Lỗi Trình Nạp", "❌ Không tìm thấy hàm CLOUD_UPDATER được truyền từ bộ nạp manager.py!")

        btn_check_update = tk.Button(t_sys, text="🔄 KIỂM TRA BẢN CẬP NHẬT TRÊN GITHUB", font=("Segoe UI", 9, "bold"), bg="#1e293b", fg="white", relief=tk.FLAT, command=kick_hoat_manual_update)
        btn_check_update.pack(pady=35, ipady=5, ipadx=10)
        self.bind_hover_animation(btn_check_update, self.ui["accent"], "#1e293b")

        def save_all_settings():
            self.os_core.user_config["theme_color"] = cb_color.get()
            self.os_core.user_config["temp_warning_limit"] = scale_warn.get()
            self.os_core.save_local_state_file()
            self.refresh_ui_colors()
            self.draw_desktop_icons()
            messagebox.showinfo("Đồng Bộ", "✅ Lưu cấu hình vào dữ liệu data.json thành công!")
            win.destroy()
            
        tk.Button(win, text="💾 LƯU THAY ĐỔI VÀ ĐỒNG BỘ", font=("Segoe UI", 9, "bold"), bg=self.ui["success"], fg="black", relief=tk.FLAT, command=save_all_settings).pack(pady=15)
        win.protocol("WM_DELETE_WINDOW", lambda: [self.running_processes.remove("Settings.exe") if "Settings.exe" in self.running_processes else None, win.destroy()])

# =====================================================================
# 4. LỚP CẦU NỐI ĐIỀU KHIỂN PHẦN CỨNG MÁY ẢO BẬT MÀN HÌNH
# =====================================================================
class ComputerHardwareController:
    def __init__(self):
        self.ram_buffer = LTPOperatingSystem()
        
    def turn_on_display(self):
        root = tk.Tk()
        root.title("LTTP.OS Virtual Machine Core Runtime Engine")
        
        def on_hardware_shutdown():
            self.ram_buffer.save_local_state_file()
            root.destroy()
            sys.exit(0)
            
        root.protocol("WM_DELETE_WINDOW", on_hardware_shutdown)
        runtime_os = LttpOSRuntime(root, self.ram_buffer, save_callback=self.ram_buffer.save_local_state_file)
        root.mainloop()
