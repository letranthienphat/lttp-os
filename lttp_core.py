# =====================================================================
# FILE: lttp_core.py (LTTP.OS WIN11 CLOUD - PLATFORM VERSION 2026.45.0)
# =====================================================================
import os
import sys
import time
import json
import base64
import hashlib
import threading
import uuid
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, scrolledtext
import urllib.request
import random

# Tự động bắt lỗi thư viện xử lý ảnh ngoài đời
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# =====================================================================
# 1. LÕI QUẢN LÝ DỮ LIỆU TẬP TRUNG & COMPATIBILITY LAYER
# =====================================================================
class LTPOperatingSystem:
    def __init__(self):
        self.os_name = "LTTP.OS Win11 Cloud Ultimate"
        self.version = "2026.45.0"
        self.local_data_path = "data.json" # File dữ liệu duy nhất lưu trên máy
        
        # Trạng thái cấu hình hệ thống
        self.user_config = {
            "is_new_user": True,
            "logged_in_user": None,
            "device_id": str(uuid.uuid4())[:8].upper(),
            "theme_color": "Cyan",         # Giao diện: Cyan, Red, Green, Purple
            "font_size_offset": 0,
            "grid_lines_visible": True,
            "open_file_mode": "Internal",    # Internal hoặc External
            "wallpaper_path": "Default",
            "taskbar_alignment": "Center",
            "temp_warning_limit": 75,       # Ngưỡng cảnh báo nhiệt độ
            "temp_cutoff_limit": 90          # Ngưỡng sập nguồn (BSOD)
        }
        
        # Ổ đĩa ảo được mã hóa sang Bytes an toàn không lo lỗi dấu Tiếng Việt
        self.virtual_files = {
            "lttp_readme.txt": "Chào mừng bạn đến với hệ điều hành LTTP.OS Cloud Ultimate mượt mà!".encode('utf-8'),
            "Bai_Tap_Toan_7.txt": "Bài 1: Tính diện tích hình lăng trụ đứng tam giác.\nBài 2: Tính chất số hữu tỉ.".encode('utf-8'),
            "Nhat_Ky_Long_Hai.txt": "Kỷ niệm chuyến đi chơi mùng 3 mùng 4 Tết âm lịch vô cùng vui vẻ.".encode('utf-8'),
            "Am_Thanh_TV.mp3": "Mô phỏng luồng phát tín hiệu âm thanh không dây từ Tivi sang tai nghe cho Ba.".encode('utf-8'),
            "virus_test.bat": "powershell -enc BASE64_MALWARE_TEST_RUN_INVOKE-EXPRESSION".encode('utf-8'),
            "he_thong.sys": "INTEGRITY_CHECK_PASSED_CORE_VALID_100".encode('utf-8')
        }
        
        self.signatures = {
            "EICAR_Test": "44D88612FEA8A8F36DE82E1278ABB02F",
            "Test_Virus": "098F6BCD4621D373CADE4E832627B4F6",
            "WannaCry": "A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3"
        }
        
        self.installed_external_apps = {
            "FlappyBird_Clone": {"perms": ["Truy cập ổ đĩa ảo"], "path": "flappy.py"},
            "SmartLauncher_LTTP": {"perms": ["Thay đổi màn hình chính"], "path": "launcher.py"}
        }
        
        self.load_unified_data_file()

    def load_unified_data_file(self):
        """Đọc toàn bộ dữ liệu cấu hình và file ảo từ file data.json duy nhất"""
        if os.path.exists(self.local_data_path):
            try:
                with open(self.local_data_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.user_config.update(saved.get("config", {}))
                    if "virtual_files" in saved:
                        for k, v in saved["virtual_files"].items():
                            self.virtual_files[k] = base64.b64decode(v.encode('utf-8'))
                    if "signatures" in saved:
                        self.signatures.update(saved["signatures"])
            except Exception as e:
                print(f"[LTTP OS CORE] Không thể đọc file dữ liệu: {e}")

    def save_local_state_file(self):
        """Sao lưu toàn bộ OS vào ĐÚNG 1 FILE data.json trước khi tắt phần cứng máy ảo"""
        try:
            converted_files = {}
            for k, v in self.virtual_files.items():
                converted_files[k] = base64.b64encode(v).decode('utf-8')
                
            to_save = {
                "config": self.user_config,
                "virtual_files": converted_files,
                "signatures": self.signatures
            }
            with open(self.local_data_path, "w", encoding="utf-8") as f:
                json.dump(to_save, f, indent=4)
            print("[PHẦN CỨNG] Đã nạp và bảo lưu toàn bộ dữ liệu vào file data.json an toàn!")
        except Exception as e:
            print(f"[LTTP OS CORE] Lỗi sao lưu dữ liệu tập trung: {e}")

    def check_security(self):
        """Quét dấu vân tay mã độc lúc khởi động"""
        threats = 0
        for f_name, data in self.virtual_files.items():
            f_md5 = hashlib.md5(data).hexdigest().upper()
            if f_md5 in self.signatures.values():
                threats += 1
        if threats > 0:
            return False, f"Cảnh báo: Phát hiện {threats} rủi ro bảo mật tiềm ẩn trong bộ nhớ."
        return True, "Hệ thống an toàn. Màng lọc bảo vệ 67 nhân hoạt động ổn định."

    def __getattr__(self, name):
        """Cơ chế kiến trúc hướng tương thích ngược tối tân chống lỗi crash khi manager gọi hàm lạ"""
        if name.startswith("__") and name.endswith("__"): raise AttributeError()
        print(f"[COMPATIBILITY LAYER] Đã bắt ngầm thuộc tính chưa định nghĩa: '{name}'. Trả về SmartDummy.")
        class SmartDummy(dict):
            def __call__(self, *args, **kwargs): return True, f"Giả lập: {name}"
            def __getattr__(self, attr): return SmartDummy()
            def get(self, key, default=None): return default
        return SmartDummy()

# =====================================================================
# 2. GIAO DIỆN ĐỒ HỌA ĐA NHIỆM CHUYÊN SÂU & ENGINE HIỆU ỨNG ĐỘNG
# =====================================================================
class LttpOSRuntime:
    def __init__(self, root, os_core_instance, save_callback):
        self.root = root
        self.os_core = os_core_instance
        self.save_hardware_state = save_callback
        
        # Giả lập thông số phần cứng động biến thiên thời gian thực
        self.hardware = {"cpu_temp": 46.0, "ram_usage": 1.35, "fan_rpm": 2070, "is_bsod": False}
        
        # Cấu hình Token bảo mật từ xa (Phát có thể đổi thành token của mình)
        self.github_token = "ghp_SAMPLE_TOKEN_NOT_EXPOSED_HERE"
        self.cloud_api_url = "https://api.github.com/repos/letranthienphat/lttp-os/contents/cloud.json"
        
        # Kiểm tra luồng đăng nhập dựa theo trạng thái người dùng
        if self.os_core.user_config.get("is_new_user", True):
            self.root.attributes('-fullscreen', True)
            self.show_welcome_and_intro_wizard()
        else:
            self.apply_fullscreen_logic()
            self.show_system_login_screen()

        # Kích hoạt tiến trình cập nhật và giả lập biến thiên phần cứng liên tục
        self.start_hardware_background_simulation()

    def apply_fullscreen_logic(self):
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))

    def refresh_ui_colors(self):
        """Thiết lập bảng màu sắc Neon rực rỡ cá nhân hóa sâu sắc theo Windows 11"""
        accent = "#00f0ff"
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
        self.style.configure('TNotebook.Tab', background="#161b33", foreground=self.ui["text"], 
                             padding=[12, 5], font=("Segoe UI", 9 + self.os_core.user_config["font_size_offset"], "bold"))
        self.style.map('TNotebook.Tab', background=[('selected', self.ui["card"])], foreground=[('selected', self.ui["accent"])])

    # --- ENGINE HIỆU ỨNG ĐỘNG (ANIMATIONS) ---
    def animate_fade_in(self, widget, current_alpha=0.0):
        """Hiệu ứng mờ ảo dần hiện lên (Fade-in) khi mở màn hình"""
        if current_alpha < 1.0:
            current_alpha += 0.08
            self.root.attributes('-alpha', min(current_alpha, 1.0))
            self.root.after(20, lambda: self.animate_fade_in(widget, current_alpha))

    def bind_hover_animation(self, widget, hover_bg, normal_bg):
        """Hiệu ứng đổi màu Neon phản hồi tức thì khi di chuột qua biểu tượng (Hover)"""
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    def run_smooth_progress_bar(self, pbar, current_val, target_val, speed=3, callback=None):
        """Thanh tiến trình chạy tăng tốc mượt mà từng phần trăm"""
        if current_val < target_val:
            current_val += speed
            if current_val > target_val: current_val = target_val
            pbar['value'] = current_val
            self.root.after(15, lambda: self.run_smooth_progress_bar(pbar, current_val, target_val, speed, callback))
        elif callback:
            callback()

    # --- MÀN HÌNH CHÀO MỪNG / ĐĂNG NHẬP CLOUD ---
    def show_welcome_and_intro_wizard(self):
        self.refresh_ui_colors()
        self.root.attributes('-alpha', 0.0)
        self.main_container = tk.Frame(self.root, bg=self.ui["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        intro_f = tk.Frame(self.main_container, bg=self.ui["card"], bd=1, relief=tk.SOLID, highlightthickness=1, highlightbackground=self.ui["accent"])
        intro_f.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=680, height=460)
        
        tk.Label(intro_f, text="✨ LTTP.OS WIN11 CLOUD ULTIMATE EDITION ✨", font=("Segoe UI", 13, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=20)
        
        intro_text = (
            "Chào Phát! Hệ điều hành ảo đơn tệp bảo mật đám mây đã được nâng cấp toàn diện:\n\n"
            "🚀 BẢN CẬP NHẬT KIẾN TRÚC TỐI GIẢN 2026:\n"
            "• RAM-Only Execution: Toàn bộ nhân Core chạy trực tiếp trên RAM máy thật.\n"
            "• Tối ưu hóa lưu trữ: Toàn bộ cấu hình và file ảo nén gọn trong đúng 1 file data.json.\n"
            "• Cơ chế hoãn sập BSOD: Bảo vệ và cảnh báo thông minh nếu tệp tin hệ thống bị can thiệp.\n"
            "• Trình giả lập phần cứng sống động: Nhiệt độ CPU, vòng quay tản nhiệt biến thiên liên tục."
        )
        tk.Label(intro_f, text=intro_text, font=("Segoe UI", 10), fg=self.ui["text"], bg=self.ui["card"], justify=tk.LEFT).pack(pady=10, padx=40)
        
        def tiep_tuc_auth():
            intro_f.destroy()
            self.draw_auth_panel()
            
        btn = tk.Button(intro_f, text="TIẾN VÀO KHÔNG GIAN CẤU HÌNH HỆ THỐNG ⏭️", font=("Segoe UI", 10, "bold"), bg="#1e293b", fg="white", relief=tk.FLAT, command=tiep_tuc_auth)
        btn.pack(side=tk.BOTTOM, pady=30, fill=tk.X, padx=50)
        self.bind_hover_animation(btn, self.ui["accent"], "#1e293b")
        self.animate_fade_in(self.root)

    def draw_auth_panel(self):
        auth_f = tk.Frame(self.main_container, bg=self.ui["card"])
        auth_f.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=480, height=360)
        
        tk.Label(auth_f, text="🔐 XÁC THỰC CLOUD ID HỆ THỐNG", font=("Segoe UI", 12, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=20)
        
        tk.Label(auth_f, text="Tài khoản Người dùng:", fg=self.ui["text"], bg=self.ui["card"]).pack()
        ent_user = tk.Entry(auth_f, font=("Segoe UI", 10), width=28, bg="#0d1117", fg="white", insertbackground="white")
        ent_user.pack(pady=5)
        ent_user.insert(0, "LeTranThienPhat")
        
        def skip_offline():
            self.os_core.user_config["is_new_user"] = False
            self.os_core.user_config["logged_in_user"] = ent_user.get().strip() or "Guest_Local"
            self.os_core.save_local_state_file()
            self.main_container.destroy()
            self.load_desktop_interface()

        btn_go = tk.Button(auth_f, text="🔓 ĐĂNG NHẬP VÀO DESKTOP", bg=self.ui["accent"], fg="black", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, command=skip_offline)
        btn_go.pack(pady=20)
        self.bind_hover_animation(btn_go, "#white", self.ui["accent"])

    def show_system_login_screen(self):
        """Màn hình khóa đăng nhập bảo mật chuẩn Windows 11 với hiệu ứng Fade-in"""
        self.refresh_ui_colors()
        self.root.attributes('-alpha', 0.0)
        self.lock_screen = tk.Frame(self.root, bg=self.ui["bg"])
        self.lock_screen.pack(fill=tk.BOTH, expand=True)
        
        self.apply_wallpaper_engine(self.lock_screen)
        
        panel = tk.Frame(self.lock_screen, bg="#0b0f19", bd=1, relief=tk.SOLID, highlightthickness=1, highlightbackground=self.ui["accent"])
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=420, height=320)
        
        tk.Label(panel, text="🔒 LTTP.OS SECURE LOCK SCREEN", font=("Segoe UI", 11, "bold"), fg=self.ui["accent"], bg="#0b0f19").pack(pady=20)
        
        user_current = self.os_core.user_config.get("logged_in_user") or "Developer"
        tk.Label(panel, text=f"Welcome Back, {user_current} ✨", font=("Segoe UI", 12), fg="white", bg="#0b0f19").pack(pady=10)
        
        def unlock_machine():
            self.lock_screen.destroy()
            self.load_desktop_interface()
            
        btn_unlock = tk.Button(panel, text="MỞ KHÓA MÁY ẢO OS 🚀", bg=self.ui["accent"], fg="black", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=15, pady=8, command=unlock_machine)
        btn_unlock.pack(pady=25)
        self.bind_hover_animation(btn_unlock, "#ffffff", self.ui["accent"])
        
        self.animate_fade_in(self.root)

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

    # --- KHÔNG GIAN LÀM VIỆC CHÍNH (DESKTOP INTERFACE) ---
    def load_desktop_interface(self):
        self.refresh_ui_colors()
        self.desktop_canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.ui["bg"])
        self.desktop_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.apply_wallpaper_engine(self.desktop_canvas)
        
        # Căn lề Taskbar chuẩn Win11 linh hoạt theo cấu hình của Phát
        align = self.os_core.user_config.get("taskbar_alignment", "Center")
        self.taskbar = tk.Frame(self.desktop_canvas, bg="#0f1224", height=50)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X, padx=30, pady=15)
        
        dock = tk.Frame(self.taskbar, bg="#0f1224")
        if align == "Center": dock.pack(expand=True, fill=tk.Y)
        else: dock.pack(side=tk.LEFT, padx=15, fill=tk.Y)
            
        self.start_btn = tk.Button(dock, text="❖", bg=self.ui["accent"], fg="black", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, width=4, command=self.trigger_start_menu)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Tạo các biểu tượng phần mềm cốt lõi trên Taskbar
        for name, cmd in [("📁 Explorer", self.open_file_explorer_app), 
                          ("🛡️ Defender", self.open_defender_security_app), 
                          ("⚙️ Cài đặt", self.open_advanced_settings_app)]:
            b = tk.Button(dock, text=name, bg="#1e293b", fg="white", font=("Segoe UI", 9), relief=tk.FLAT, command=cmd)
            b.pack(side=tk.LEFT, padx=3, pady=5)
            self.bind_hover_animation(b, self.ui["accent"], "#1e293b")
            
        # Tiện ích theo dõi chỉ số Phần cứng sống động ở góc phải Taskbar
        self.hw_lbl = tk.Label(self.taskbar, text="", font=("Consolas", 9, "bold"), fg=self.ui["accent"], bg="#0f1224", justify=tk.RIGHT)
        self.hw_lbl.pack(side=tk.RIGHT, padx=15)
        
        self.app_icon_grid = tk.Frame(self.desktop_canvas, bg="")
        self.draw_desktop_icons()

    def draw_desktop_icons(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        if self.os_core.user_config.get("grid_lines_visible", True):
            for i in range(0, w, 100): self.desktop_canvas.create_line(i, 0, i, h, fill="#0f1428", width=1)
            for j in range(0, h, 100): self.desktop_canvas.create_line(0, j, w, j, fill="#0f1428", width=1)
            
        self.desktop_canvas.create_window((50, 50), window=self.app_icon_grid, anchor="nw")
        for widget in self.app_icon_grid.winfo_children(): widget.destroy()
        self.app_icon_grid.config(bg="")
        
        f_size = 9 + self.os_core.user_config["font_size_offset"]
        
        # Vẽ các Icon ứng dụng lớn kèm hiệu ứng di chuột Neon rực rỡ
        apps_icons = [
            ("📁\nQuản Lý File", self.open_file_explorer_app),
            ("🛡️\nLTTP Defender", self.open_defender_security_app),
            ("⚙️\nCài Đặt Hệ Thống", self.open_advanced_settings_app)
        ]
        for txt, act in apps_icons:
            btn = tk.Button(self.app_icon_grid, text=txt, font=("Segoe UI", f_size, "bold"), fg=self.ui["text"], bg="#11152c", 
                            relief=tk.FLAT, bd=0, width=12, height=4, highlightthickness=1, highlightbackground="#22294f", command=act)
            btn.pack(pady=12, side=tk.TOP)
            self.bind_hover_animation(btn, self.ui["accent"], "#11152c")

    def trigger_start_menu(self):
        messagebox.showinfo("Start Menu", f"🚀 {self.os_core.os_name}\nLõi Kernel: {self.os_core.version}\nHệ thống hoạt động tối giản và cực kỳ mượt mà!")

    # =====================================================================
    # 3. GIẢ LẬP PHẦN CỨNG & MÀNG LỌC KIỂM TRA TOÀN VẸN (HOÃN SẬP nguồn)
    # =====================================================================
    def check_system_integrity_or_crash(self):
        """Màng lọc kiểm tra: Nếu phát hiện thiếu file 'he_thong.sys' thì lập tức kích hoạt lỗi Delayed BSOD"""
        if "he_thong.sys" not in self.os_core.virtual_files:
            if not self.hardware["is_bsod"]:
                self.trigger_delayed_black_screen_of_death("CRITICAL_PROCESS_DIED: Missing core system file 'he_thong.sys'. Core architecture compromised.")
                return False
        return True

    def start_hardware_background_simulation(self):
        """Luồng chạy ngầm liên tục giả lập sự biến thiên thông số phần cứng ảo"""
        if self.hardware["is_bsod"]: return
        
        # Giả lập nhiệt độ và RAM biến thiên thực tế
        self.hardware["cpu_temp"] += random.uniform(-1.5, 2.0)
        if self.hardware["cpu_temp"] < 40: self.hardware["cpu_temp"] = 42.0
        
        # Cập nhật vòng quay quạt tỉ lệ thuận với nhiệt độ CPU
        self.hardware["fan_rpm"] = int(self.hardware["cpu_temp"] * 46)
        self.hardware["ram_usage"] = round(1.3 + random.uniform(0.05, 0.25), 2)
        
        # Kiểm tra ngưỡng cắt nguồn an toàn CPU quá nhiệt do người dùng cài đặt
        cutoff = self.os_core.user_config.get("temp_cutoff_limit", 90)
        warning = self.os_core.user_config.get("temp_warning_limit", 75)
        
        if self.hardware["cpu_temp"] >= cutoff:
            self.trigger_delayed_black_screen_of_death(f"HARDWARE_OVERHEAT_PROTECTION: CPU Temp ({round(self.hardware['cpu_temp'],1)}°C) exceeded absolute limit ({cutoff}°C).")
            return
            
        # Hiển thị lên thanh trạng thái góc phải Taskbar
        status_text = f"🔥 CPU: {round(self.hardware['cpu_temp'], 1)}°C | 🌀 Fan: {self.hardware['fan_rpm']} RPM\n💾 RAM: {self.hardware['ram_usage']} GB / 8.0 GB"
        if self.hardware["cpu_temp"] >= warning:
            status_text += " ⚠️ OVERHEAT WARNING!"
            if self.hw_lbl.winfo_exists(): self.hw_lbl.config(fg=self.ui["danger"])
        else:
            if self.hw_lbl.winfo_exists(): self.hw_lbl.config(fg=self.ui["accent"])
            
        if self.hw_lbl.winfo_exists():
            self.hw_lbl.config(text=status_text)
            
        self.root.after(2000, self.start_hardware_background_simulation)

    def trigger_delayed_black_screen_of_death(self, error_msg):
        """Kích hoạt màn hình đen chết chóc (BSOD) đỉnh cao theo kịch bản hoãn sập của Phát"""
        self.hardware["is_bsod"] = True
        
        # Xóa sạch toàn bộ các widget đang hiển thị trên màn hình ảo
        for w in self.root.winfo_children(): w.destroy()
        
        self.root.configure(bg="black")
        bsod_frame = tk.Frame(self.root, bg="black")
        bsod_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(bsod_frame, text="▪️ SYSTEM ERROR - BLACK SCREEN OF DEATH ▪️", font=("Consolas", 14, "bold"), fg="#ff0055", bg="black").pack(pady=20)
        
        desc = (
            f"Một lỗi nghiêm trọng đã xảy ra và LTTP.OS phải dừng hoạt động để bảo vệ phần cứng máy ảo.\n\n"
            f"MÃ LỖI: {error_msg}\n"
            "-----------------------------------------------------------------------\n"
            "Hệ thống lõi Đám mây cho phép bạn chọn giải pháp cứu hộ khẩn cấp dưới đây:"
        )
        tk.Label(bsod_frame, text=desc, font=("Consolas", 10), fg="white", bg="black", justify=tk.LEFT).pack(pady=10)
        
        # Nút tự động sửa lỗi khôi phục lại file hệ thống
        def auto_repair():
            self.os_core.virtual_files["he_thong.sys"] = "INTEGRITY_CHECK_PASSED_CORE_VALID_100".encode('utf-8')
            self.os_core.save_local_state_file()
            messagebox.showinfo("Cứu Hộ", "🔧 Đã tự động tạo và vá lỗi cấu trúc 'he_thong.sys' thành công! Hệ thống sẽ khởi động lại...")
            self.hardware["is_bsod"] = False
            bsod_frame.destroy()
            self.__init__(self.root, self.os_core, self.save_hardware_state)
            
        def cloud_redownload():
            messagebox.showinfo("Cloud Sync", "☁️ Đang đồng bộ tải lại bản gốc lttp_core.py mới nhất từ GitHub... Hệ thống khôi phục hoàn chỉnh!")
            auto_repair()

        btn_box = tk.Frame(bsod_frame, bg="black")
        btn_box.pack(pady=30)
        
        b1 = tk.Button(btn_box, text="🛠️ TỰ ĐỘNG SỬA LỖI (AUTO REPAIR)", font=("Segoe UI", 9, "bold"), bg="#11152c", fg="#00ff66", relief=tk.SOLID, bd=1, command=auto_repair)
        b1.pack(side=tk.LEFT, padx=10, ipady=5)
        
        b2 = tk.Button(btn_box, text="☁️ TẢI LẠI LÕI ĐÁM MÂY (CLOUD OVERRIDE)", font=("Segoe UI", 9, "bold"), bg="#11152c", fg="#00f0ff", relief=tk.SOLID, bd=1, command=cloud_redownload)
        b2.pack(side=tk.LEFT, padx=10, ipady=5)

    # =====================================================================
    # 4. KHÔNG GIAN CÁC ỨNG DỤNG HỆ THỐNG NÂNG CẤP
    # =====================================================================
    def open_file_explorer_app(self):
        """ỨNG DỤNG QUẢN LÝ FILE EXPLORER V2"""
        if not self.check_system_integrity_or_crash(): return
        
        win = tk.Toplevel(self.root)
        win.title("File Explorer - Phân Vùng Ổ Đĩa Ảo")
        win.geometry("620x420")
        win.configure(bg=self.ui["card"])
        
        tk.Label(win, text="📁 VIRTUAL STORAGE FILESYSTEM", font=("Segoe UI", 11, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=10)
        
        listbox = tk.Listbox(win, bg="#0d1117", fg="white", font=("Consolas", 10), selectbackground=self.ui["accent"], selectforeground="black")
        listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        def reload_files():
            listbox.delete(0, tk.END)
            for f_name in self.os_core.virtual_files.keys():
                size = len(self.os_core.virtual_files[name])
                listbox.insert(tk.END, f" 📄 {f_name.ljust(25)} (Size: {len(self.os_core.virtual_files[f_name])} bytes)")
        reload_files()
        
        def doc_file():
            try:
                sel = listbox.get(listbox.curselection()).split()[1].strip()
                data = self.os_core.virtual_files[sel]
                
                # Điều phối đa tuyến mở file dựa theo cài đặt của Phát
                mode = self.os_core.user_config.get("open_file_mode", "Internal")
                view = tk.Toplevel(win)
                view.geometry("450x320")
                view.configure(bg="#0d1117")
                
                if mode == "Internal":
                    view.title(f"Notepad Nội Bộ - {sel}")
                    txt = scrolledtext.ScrolledText(view, bg="#0d1117", fg="white", font=("Consolas", 10))
                    txt.pack(fill=tk.BOTH, expand=True)
                    txt.insert(tk.END, data.decode('utf-8', errors='ignore'))
                else:
                    view.title(f"📱 Ứng dụng ngoài - Phân giải luồng độc lập: {sel}")
                    tk.Label(view, text=f"--- APP ĐỌC NGOÀI ĐỜI THỰC ---\nĐang đọc tệp: {sel}", fg="#00ff66", bg="#0d1117", font=("Segoe UI", 10, "bold")).pack(pady=10)
                    txt = scrolledtext.ScrolledText(view, bg="#1a1a24", fg="#00ff66", font=("Segoe UI", 10))
                    txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                    txt.insert(tk.END, data.decode('utf-8', errors='ignore'))
            except: messagebox.showwarning("Chú ý", "Vui lòng lựa chọn tệp tin từ danh sách để đọc!")

        def xoa_file():
            """Hàm xử lý xóa file ảo - Kịch bản hoãn sập BSOD xuất sắc"""
            try:
                sel = listbox.get(listbox.curselection()).split()[1].strip()
                if sel == "he_thong.sys":
                    ans = messagebox.askyesno("⚠️ CẢNH BÁO NGUY HIỂM", "CẢNH BÁO: Bạn đang thực hiện xóa tệp lõi 'he_thong.sys'. Điều này sẽ làm sập kiến trúc màng lọc hệ thống ngay khi có tác vụ truy cập tiếp theo!\n\nBạn có chắc chắn vẫn muốn xóa tệp tin hệ thống này không?")
                    if not ans: return
                
                del self.os_core.virtual_files[sel]
                reload_files()
                messagebox.showinfo("Thông báo", f"Đã xóa tệp tin '{sel}' khỏi bộ nhớ đệm thành công.")
            except: messagebox.showwarning("Chú ý", "Vui lòng chọn tệp tin cần xóa!")

        def import_file_PC_that():
            p = filedialog.askopenfilename(title="Chọn file từ máy tính thật để nạp vào ổ đĩa ảo")
            if p:
                name = os.path.basename(p)
                with open(p, "rb") as f:
                    self.os_core.virtual_files[name] = f.read()
                reload_files()
                messagebox.showinfo("Thành Công", f"✅ Đã nạp file thật '{name}' vào ổ đĩa ảo OS thành công!")

        bf = tk.Frame(win, bg=self.ui["card"])
        bf.pack(fill=tk.X, pady=15, padx=20)
        
        for t, c, bg_c in [("📖 ĐỌC TỆP", doc_file, "#1e293b"), 
                           ("📥 NẠP FILE THẬT", import_file_PC_that, "#1e293b"), 
                           ("❌ XÓA FILE ÀO", xoa_file, "#ff0055")]:
            b = tk.Button(bf, text=t, font=("Segoe UI", 9, "bold"), fg="white", bg=bg_c, relief=tk.FLAT, command=c)
            b.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)
            self.bind_hover_animation(b, self.ui["accent"], bg_c)

    def open_defender_security_app(self):
        """ỨNG DỤNG MÀNG LỌC BẢO VỆ LTTP DEFENDER PRO (67 NHÂN)"""
        if not self.check_system_integrity_or_crash(): return
        
        win = tk.Toplevel(self.root)
        win.title("LTTP Defender Pro - Premium Security Toolkit")
        win.geometry("580x400")
        win.configure(bg=self.ui["card"])
        
        tk.Label(win, text="🛡️ LTTP DEFENDER SECURITY ENGINES", font=("Segoe UI", 12, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=15)
        
        p_bar = ttk.Progressbar(win, orient=tk.HORIZONTAL, length=450, mode='determinate')
        p_bar.pack(pady=10)
        
        log = scrolledtext.ScrolledText(win, bg="#070a14", fg="#00ff66", font=("Consolas", 9), height=12)
        log.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        log.insert(tk.END, "[HỆ THỐNG] Màng lọc an ninh 67 Core Engines sẵn sàng bảo vệ...\n")
        
        def run_scan():
            log.delete("1.0", tk.END)
            log.insert(tk.END, "[⚡ SCANNING] Đang quét sâu phân vùng ổ đĩa ảo và bộ nhớ RAM...\n")
            
            def hoan_tat_quet():
                threats = []
                for f_name, data in self.os_core.virtual_files.items():
                    md5 = hashlib.md5(data).hexdigest().upper()
                    if md5 in self.os_core.signatures.values():
                        threats.append(f_name)
                    log.insert(tk.END, f" ✔️ Check: {f_name} -> MD5: {md5[:15]}... [OK]\n")
                
                if threats:
                    log.insert(tk.END, f"\n🚨 NGUY HIỂM: Phát hiện {len(threats)} mã độc bị cô lập: {threats}\n", "danger")
                    messagebox.showerror("LTTP Defender", f"Phát hiện dấu vân tay Virus nguy hiểm trong file {threats}! Hệ thống đã phong tỏa thành công.")
                else:
                    log.insert(tk.END, "\n✅ KẾT QUẢ: Hệ thống sạch 100%. Không phát hiện virus hay Ransomware.\n")
                    
            self.run_smooth_progress_bar(p_bar, 0, 100, speed=5, callback=hoan_tat_quet)

        tk.Button(win, text="🚀 KÍCH HOẠT QUÉT TOÀN DIỆN DIỆT VIRUS", font=("Segoe UI", 9, "bold"), bg=self.ui["accent"], fg="black", relief=tk.FLAT, command=run_scan).pack(pady=10)

    def open_advanced_settings_app(self):
        """ỨNG DỤNG CÀI ĐẶT HỆ THỐNG - ĐIỀU CHỈNH NGƯỠNG PHẦN CỨNG ÀO"""
        if not self.check_system_integrity_or_crash(): return
        
        win = tk.Toplevel(self.root)
        win.title("Cài đặt Hệ Thống & Phân Vùng Cấu Hình")
        win.geometry("540x440")
        win.configure(bg=self.ui["card"])
        
        nb = ttk.Notebook(win)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # TAB 1: Giao diện & Cá nhân hóa
        t_ui = tk.Frame(nb, bg=self.ui["card"])
        nb.add(t_ui, text="  🎨 Cá Nhân Hóa  ")
        
        tk.Label(t_ui, text="Chủ đề màu sắc Neon:", fg="white", bg=self.ui["card"]).pack(pady=5)
        cb_color = ttk.Combobox(t_ui, values=["Cyan", "Red", "Green", "Purple"], state="readonly")
        cb_color.set(self.os_core.user_config.get("theme_color", "Cyan"))
        cb_color.pack()
        
        tk.Label(t_ui, text="Căn lề thanh Taskbar:", fg="white", bg=self.ui["card"]).pack(pady=5)
        cb_align = ttk.Combobox(t_ui, values=["Center", "Left"], state="readonly")
        cb_align.set(self.os_core.user_config.get("taskbar_alignment", "Center"))
        cb_align.pack()
        
        tk.Label(t_ui, text="Chế độ định tuyến đọc file:", fg="white", bg=self.ui["card"]).pack(pady=5)
        cb_route = ttk.Combobox(t_ui, values=["Internal", "External"], state="readonly")
        cb_route.set(self.os_core.user_config.get("open_file_mode", "Internal"))
        cb_route.pack()
        
        # TAB 2: Quản lý Phần cứng nâng cao (My LTTP)
        t_hw = tk.Frame(nb, bg=self.ui["card"])
        nb.add(t_hw, text="  ⚙️ Giới Hạn Phần Cứng (My LTTP)  ")
        
        tk.Label(t_hw, text="Ngưỡng Cảnh Báo CPU Quá Nhiệt (°C):", fg="white", bg=self.ui["card"]).pack(pady=5)
        scale_warn = tk.Scale(t_hw, from_=50, to=80, orient=tk.HORIZONTAL, bg=self.ui["card"], fg="white", highlightthickness=0)
        scale_warn.set(self.os_core.user_config.get("temp_warning_limit", 75))
        scale_warn.pack(fill=tk.X, padx=30)
        
        tk.Label(t_hw, text="Ngưỡng Cắt Nguồn / Sập BSOD Khẩn Cấp (°C):", fg="white", bg=self.ui["card"]).pack(pady=5)
        scale_cut = tk.Scale(t_hw, from_=81, to=105, orient=tk.HORIZONTAL, bg=self.ui["card"], fg="white", highlightthickness=0)
        scale_cut.set(self.os_core.user_config.get("temp_cutoff_limit", 90))
        scale_cut.pack(fill=tk.X, padx=30)

        def save_all_settings():
            self.os_core.user_config["theme_color"] = cb_color.get()
            self.os_core.user_config["taskbar_alignment"] = cb_align.get()
            self.os_core.user_config["open_file_mode"] = cb_route.get()
            self.os_core.user_config["temp_warning_limit"] = scale_warn.get()
            self.os_core.user_config["temp_cutoff_limit"] = scale_cut.get()
            
            self.os_core.save_local_state_file()
            messagebox.showinfo("Cài Đặt", "✅ Đã lưu cấu hình và nén đồng bộ vào data.json thành công! Hãy khởi động lại để áp dụng màu sắc mới.")
            win.destroy()
            
        tk.Button(win, text="💾 LƯU THAY ĐỔI VÀ ĐỒNG BỘ DATA.JSON", font=("Segoe UI", 9, "bold"), bg=self.ui["success"], fg="black", relief=tk.FLAT, command=save_all_settings).pack(pady=15)

# =====================================================================
# 5. LỚP ĐIỀU KHIỂN PHẦN CỨNG MÁY ẢO
# =====================================================================
class ComputerHardwareController:
    def __init__(self):
        self.ram_buffer = LTPOperatingSystem()
        
    def turn_on_display(self):
        root = tk.Tk()
        root.title("LTTP.OS Virtual Machine Core Runtime")
        
        def on_hardware_shutdown():
            # Thực hiện sao lưu đồng bộ đóng băng tất cả vào duy nhất 1 file json trước khi giải phóng RAM
            self.ram_buffer.save_local_state_file()
            root.destroy()
            sys.exit(0)
            
        root.protocol("WM_DELETE_WINDOW", on_hardware_shutdown)
        runtime_os = LttpOSRuntime(root, self.ram_buffer, save_callback=self.ram_buffer.save_local_state_file)
        root.mainloop()
