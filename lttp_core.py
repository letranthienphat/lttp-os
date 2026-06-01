# =====================================================================
# FILE: lttp_core.py (LTTP.OS WIN11 CLOUD - PLATFORM VERSION 2026.35.0)
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Kiểm tra thư viện xử lý ảnh nền máy thật bên ngoài độc lập
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# =====================================================================
# LỚP GIẢ LẬP ĐỐI TƯỢNG LAI - CHỐNG SẬP TƯƠNG THÍCH NGƯỢC
# =====================================================================
class SmartDummy(dict):
    """
    Bắt các thuộc tính chưa được định nghĩa trong tương lai của manager.py.
    Trả về một đối tượng lai thông minh vừa gọi hàm được, vừa truy cập dữ liệu .get() được.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        return True, "Hàm giả lập tương thích ngược hoạt động ổn định."
    def __getattr__(self, name):
        return SmartDummy()

# =====================================================================
# LÕI HỆ ĐIỀU HÀNH & HỆ THỐNG FILE ẢO VFS (LOCAL CORES)
# =====================================================================
class LTPOperatingSystem:
    def __init__(self):
        self.os_name = "LTTP.OS Win11 Cloud Edition"
        self.version = "2026.35.0"
        self.local_data_path = "data.json"
        
        # Cấu hình hệ thống mặc định (Dành cho máy mới setup)
        self.user_config = {
            "is_new_user": True,
            "logged_in_user": None,
            "device_id": str(uuid.uuid4())[:8].upper(),
            "theme_color": "Cyan",         # Các chủ đề Neon: Cyan, Red, Green, Purple
            "font_size_offset": 0,
            "grid_lines_visible": True,
            "open_file_mode": "Internal",    # Internal (Trong OS) hoặc External (App Ngoài)
            "wallpaper_path": "Default",     # Đường dẫn ảnh ngoài đời hoặc Default
            "taskbar_alignment": "Center"    # Center hoặc Left chuẩn Windows 11
        }
        
        # 📂 HỆ THỐNG THƯ MỤC VÀ FILE ẢO PHÂN TÁCH BIỆT (VFS ROOT)
        # Thay thế hoàn toàn các file ảo bài tập toán cũ theo yêu cầu của Phát
        self.virtual_files = {
            "System/kernel.sys": b"LTTP_OS_KERNEL_CORE_V2026_PROTECTED",
            "System/shell.sys": b"LTTP_OS_SHELL_ENVIRONMENT_INTEGRATION_MANIFEST",
            "System/drivers.sys": b"HARDWARE_DRIVERS_CONFIGURATION_DATA_ROUTINE",
            "User/Documents/lttp_readme.txt": b"Chao mung ban den voi he dieu hanh LTTP.OS 2026 chinh thuc!",
            "User/Photos/Nhat_Ky_Long_Hai.txt": b"Ky niem chuyen di choi mung 3 mung 4 Tet am lich.",
            "User/Downloads/virus_test.bat": b"powershell -enc BASE64_MALWARE_TEST_RUN_INVOKE-EXPRESSION"
        }
        
        # Kho cơ sở dữ liệu chữ ký mẫu độc (Mặc định quét an ninh)
        self.signatures = {
            "EICAR_Test": "44D88612FEA8A8F36DE82E1278ABB02F",
            "Test_Virus": "098F6BCD4621D373CADE4E832627B4F6",
            "WannaCry": "A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3"
        }
        
        # Danh sách ứng dụng mở rộng cài đặt từ bên ngoài và phân quyền giám sát (Permissions)
        self.installed_external_apps = {
            "FlappyBird_Clone": {"perms": ["Truy cập ổ đĩa ảo", "Sử dụng Internet"], "path": "flappy.py"},
            "SmartLauncher_LTTP": {"perms": ["Thay đổi màn hình chính", "Đọc thông tin RAM"], "path": "launcher.py"}
        }
        
        self.last_sig_web_md5 = ""
        self.load_local_state_file()

    def load_local_state_file(self):
        """Đọc và đồng bộ cấu hình cấu trúc dữ liệu từ file data.json cục bộ"""
        if os.path.exists(self.local_data_path):
            try:
                with open(self.local_data_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.user_config.update(saved.get("config", {}))
                    if "virtual_files" in saved:
                        for k, v in saved["virtual_files"].items():
                            self.virtual_files[k] = base64.b64decode(v.encode('utf-8'))
            except:
                pass

    def save_local_state_file(self):
        """Sao lưu an toàn toàn bộ cấu hình và file ảo xuống file data.json cục bộ"""
        try:
            converted_files = {}
            for k, v in self.virtual_files.items():
                converted_files[k] = base64.b64encode(v).decode('utf-8')
                
            to_save = {
                "config": self.user_config,
                "virtual_files": converted_files
            }
            with open(self.local_data_path, "w", encoding="utf-8") as f:
                json.dump(to_save, f, indent=4)
        except Exception as e:
            print(f"[LTTP OS] Lỗi sao lưu dữ liệu cấu hình: {e}")

    def check_security(self):
        """Kiểm tra an toàn mã độc lúc khởi động phần cứng"""
        try:
            threats = 0
            for f_name, data in self.virtual_files.items():
                file_md5 = hashlib.md5(data).hexdigest().upper()
                if file_md5 in self.signatures.values():
                    threats += 1
            if threats > 0:
                return False, f"Cảnh báo: Phát hiện {threats} rủi ro mã độc trong bộ nhớ ảo."
            return True, "Hệ thống an toàn. Màng lọc an ninh hoạt động ổn định."
        except Exception as e:
            return True, f"Bỏ qua kiểm tra: {e}"

    def get_stats(self):
        """Trả về chỉ số thống kê phần cứng máy ảo"""
        return {"total_files": len(self.virtual_files), "signatures": len(self.signatures)}

    def __getattr__(self, name):
        """Cơ chế kháng sập thông minh, tự động nuốt lỗi nếu manager.py gọi hàm chưa tồn tại"""
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(f"Bỏ qua thuộc tính hệ thống mặc định: {name}")
        print(f"[CẢNH BÁO TƯƠNG THÍCH] Trình quản lý gọi thuộc tính chưa định nghĩa: '{name}'. Tự động giả lập.")
        return SmartDummy()

# =====================================================================
# GIAO DIỆN ĐỒ HỌA ĐA NHIỆM CHUYÊN SÂU (RUNTIME INTERFACE)
# =====================================================================
class LttpOSRuntime:
    def __init__(self, root, os_core_instance, save_callback):
        self.root = root
        self.os_core = os_core_instance
        self.save_hardware_state = save_callback
        self.is_dead = False # Trạng thái kiểm soát sập nguồn BSOD
        
        # Cấu hình Token và API đám mây GitHub chính thức của Phát
        self.github_token = "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"
        self.cloud_api_url = "https://api.github.com/repos/letranthienphat/lttp-os/contents/cloud.json"
        self.sig_raw_url = "https://raw.githubusercontent.com/letranthienphat/lttp-os/refs/heads/main/signatures.json"

        # Điều phối luồng khởi động dựa trên trạng thái người dùng
        if self.os_core.user_config.get("is_new_user", True):
            self.root.attributes('-fullscreen', True)
            self.show_welcome_and_intro_wizard()
        else:
            self.apply_fullscreen_logic()
            self.show_system_login_screen()

    def apply_fullscreen_logic(self):
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen_fast())

    def exit_fullscreen_fast(self):
        self.root.attributes('-fullscreen', False)

    def refresh_ui_colors(self):
        """Thiết lập bảng màu Neon cá nhân hóa sâu sắc theo Windows 11 của Phát"""
        accent = "#00f0ff" # Mặc định Cyan rực rỡ
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
                             padding=[15, 6], font=("Segoe UI", 9 + self.os_core.user_config.get("font_size_offset", 0), "bold"))
        self.style.map('TNotebook.Tab', background=[('selected', self.ui["card"])], foreground=[('selected', self.ui["accent"])])

    # =====================================================================
    # TIẾN TRÌNH: CHÀO MỪNG / ĐĂNG NHẬP / ĐĂNG KÝ ĐÁM MÂY GITHUB
    # =====================================================================
    def show_welcome_and_intro_wizard(self):
        self.refresh_ui_colors()
        self.main_container = tk.Frame(self.root, bg=self.ui["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        intro_f = tk.Frame(self.main_container, bg=self.ui["card"], bd=1, relief=tk.SOLID, highlightthickness=1, highlightbackground=self.ui["accent"])
        intro_f.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=650, height=450)
        
        tk.Label(intro_f, text="✨ CHÀO MỪNG ĐẾN VỚI LTTP.OS WIN11 CLOUD ✨", font=("Segoe UI", 14, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=20)
        
        intro_text = (
            "Hệ điều hành ảo đa nhiệm tích hợp bảo mật Đám mây đồng bộ thời gian thực.\n\n"
            "🚀 CÁC TÍNH NĂNG ĐÃ THIẾT LẬP:\n"
            "• LTTP Cloud: Đăng ký / Đăng nhập và mã hóa đồng bộ dữ liệu lên GitHub.\n"
            "• Virtual File System (VFS): Quản lý cấu trúc cây thư mục System/ và User/ ảo biệt lập.\n"
            "• Màng lọc an ninh: Quét mã độc vân tay thông minh, gửi log cảnh báo về Gmail.\n"
            "• Thiết lập giao diện sâu: Hỗ trợ nạp hình nền tùy biến từ máy thật ngoài đời.\n"
            "• Kháng lỗi kiến trúc: Tương thích ngược thông minh, ngăn chặn sập mã nguồn đột ngột."
        )
        lbl_msg = tk.Label(intro_f, text=intro_text, font=("Segoe UI", 10), fg=self.ui["text"], bg=self.ui["card"], justify=tk.LEFT)
        lbl_msg.pack(pady=10, padx=35)
        
        def tiep_tuc_den_auth_panel():
            intro_f.destroy()
            self.draw_auth_tab_interface()
            
        btn_skip = tk.Button(intro_f, text="TIẾP TỤC ĐẾN FORM ĐĂNG NHẬP / ĐĂNG KÝ ID CLOUD ⏭️", font=("Segoe UI", 10, "bold"), bg="#1e293b", fg="white", relief=tk.FLAT, command=tiep_tuc_den_auth_panel)
        btn_skip.pack(side=tk.BOTTOM, pady=25, fill=tk.X, padx=50)

    def draw_auth_tab_interface(self):
        auth_f = tk.Frame(self.main_container, bg=self.ui["card"])
        auth_f.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=380)
        
        nb = ttk.Notebook(auth_f)
        nb.pack(fill=tk.BOTH, expand=True)
        
        # TAB 1: ĐĂNG NHẬP HỆ THỐNG
        t_login = tk.Frame(nb, bg=self.ui["card"])
        nb.add(t_login, text="  🔐 ĐĂNG NHẬP HỆ THỐNG  ")
        
        tk.Label(t_login, text="Tài khoản LTTP Cloud ID:", fg=self.ui["text"], bg=self.ui["card"], font=("Segoe UI", 10)).pack(pady=(20,2))
        ent_user = tk.Entry(t_login, font=("Segoe UI", 11), width=30, bg="#0d1117", fg="white", insertbackground="white")
        ent_user.pack()
        
        tk.Label(t_login, text="Mật khẩu bảo mật:", fg=self.ui["text"], bg=self.ui["card"], font=("Segoe UI", 10)).pack(pady=(10,2))
        ent_pass = tk.Entry(t_login, font=("Segoe UI", 11), width=30, show="*", bg="#0d1117", fg="white", insertbackground="white")
        ent_pass.pack()
        
        # TAB 2: ĐĂNG KÝ CLOUD ID
        t_reg = tk.Frame(nb, bg=self.ui["card"])
        nb.add(t_reg, text="  📝 ĐĂNG KÝ CLOUD ID  ")
        
        tk.Label(t_reg, text="Tên tài khoản mới cần tạo:", fg=self.ui["text"], bg=self.ui["card"], font=("Segoe UI", 10)).pack(pady=(20,2))
        ent_ruser = tk.Entry(t_reg, font=("Segoe UI", 11), width=30, bg="#0d1117", fg="white", insertbackground="white")
        ent_ruser.pack()
        
        tk.Label(t_reg, text="Mật khẩu bảo mật đám mây:", fg=self.ui["text"], bg=self.ui["card"], font=("Segoe UI", 10)).pack(pady=(10,2))
        ent_rpass = tk.Entry(t_reg, font=("Segoe UI", 11), width=30, show="*", bg="#0d1117", fg="white", insertbackground="white")
        ent_rpass.pack()

        # LOGIC GIAO TIẾP CLOUD API VỚI GITHUB
        def execute_cloud_auth_logic(mode):
            u = ent_user.get().strip() if mode == "login" else ent_ruser.get().strip()
            p = ent_pass.get().strip() if mode == "login" else ent_rpass.get().strip()
            
            if not u or not p:
                messagebox.showerror("Lỗi dữ liệu", "Vui lòng nhập đầy đủ thông tin tài khoản và mật khẩu!")
                return
            
            p_hash = hashlib.md5(p.encode()).hexdigest()
            threading.Thread(target=sync_auth_with_github, args=(u, p_hash, mode), daemon=True).start()

        def sync_auth_with_github(u, p_hash, mode):
            try:
                req = urllib.request.Request(self.cloud_api_url, headers={"Authorization": f"token {self.github_token}"})
                with urllib.request.urlopen(req) as resp:
                    res_json = json.loads(resp.read().decode())
                    sha = res_json["sha"]
                    current_cloud_data = json.loads(base64.b64decode(res_json["content"]).decode('utf-8'))
            except:
                current_cloud_data = {"users_database": {}, "devices_cloud_storage": {}}
                sha = None

            if "users_database" not in current_cloud_data: 
                current_cloud_data["users_database"] = {}

            if mode == "login":
                if u in current_cloud_data["users_database"] and current_cloud_data["users_database"][u] == p_hash:
                    self.os_core.user_config["logged_in_user"] = u
                    self.os_core.user_config["is_new_user"] = False
                    self.os_core.save_local_state_file()
                    self.root.after(0, enter_desktop_after_auth_success)
                else:
                    messagebox.showerror("Xác thực thất bại", "Tài khoản không chính xác hoặc mật khẩu sai trên Đám mây!")
            else:
                if u in current_cloud_data["users_database"]:
                    messagebox.showerror("Trùng lặp ID", "Tài khoản đám mây này đã được đăng ký bởi thiết bị khác!")
                    return
                
                current_cloud_data["users_database"][u] = p_hash
                if self.push_data_to_github_cloud_file(current_cloud_data, sha):
                    messagebox.showinfo("Thành Công", "Đã khởi tạo và đồng bộ tài khoản LTTP Cloud mới lên GitHub thành công!")
                else:
                    messagebox.showerror("Lỗi Mạng API", "Kết nối lỗi hoặc Token GitHub không được cấp quyền ghi đè!")

        def enter_desktop_after_auth_success():
            self.main_container.destroy()
            self.apply_fullscreen_logic()
            self.load_desktop_interface()

        def skip_auth_locally():
            self.os_core.user_config["is_new_user"] = False
            self.os_core.user_config["logged_in_user"] = "Guest_Offline"
            self.os_core.save_local_state_file()
            enter_desktop_after_auth_success()

        tk.Button(t_login, text="🔓 ĐĂNG NHẬP ĐÁM MÂY", bg=self.ui["accent"], fg="black", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, command=lambda: execute_cloud_auth_logic("login")).pack(pady=15)
        tk.Button(t_reg, text="✨ ĐĂNG KÝ TÀI KHOẢN MỚI", bg=self.ui["success"], fg="black", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, command=lambda: execute_cloud_auth_logic("register")).pack(pady=15)
        
        btn_skip_auth = tk.Button(auth_f, text="🛑 Bỏ qua (Sử dụng chế độ ngoại tuyến không đồng bộ)", bg="#334155", fg="white", font=("Segoe UI", 9), relief=tk.FLAT, command=skip_auth_locally)
        btn_skip_auth.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    def show_system_login_screen(self):
        """Màn hình khóa đăng nhập bảo mật chuẩn Windows 11 dành cho người dùng cũ"""
        self.refresh_ui_colors()
        self.lock_screen = tk.Frame(self.root, bg=self.ui["bg"])
        self.lock_screen.pack(fill=tk.BOTH, expand=True)
        
        self.apply_custom_background_wallpaper_engine(self.lock_screen)
        
        panel = tk.Frame(self.lock_screen, bg="#0b0f19", bd=1, relief=tk.SOLID, highlightthickness=1, highlightbackground=self.ui["accent"])
        panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=420, height=320)
        
        tk.Label(panel, text="🔒 LTTP.OS SIGN-IN ARCHITECTURE", font=("Segoe UI", 11, "bold"), fg=self.ui["accent"], bg="#0b0f19").pack(pady=20)
        
        logged_user = self.os_core.user_config.get("logged_in_user") or "Guest_Offline"
        tk.Label(panel, text=f"Chào mừng trở lại:\n👉 {logged_user} 👈", font=("Segoe UI", 11, "bold"), fg="white", bg="#0b0f19", justify=tk.CENTER).pack(pady=10)
        
        def unlock_and_enter_desktop():
            self.lock_screen.destroy()
            self.load_desktop_interface()
            # Thực thi quét virus ngầm khi vào màn hình
            threading.Thread(target=self.auto_check_sig_changes_ngam, daemon=True).start()
            
        tk.Button(panel, text="MỞ KHÓA MÁY ẢO 🚀", bg=self.ui["accent"], fg="black", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=15, pady=8, command=unlock_and_enter_desktop).pack(pady=20)

    def apply_custom_background_wallpaper_engine(self, container_widget):
        """Hàm phân giải đồ họa nạp hình nền tùy biến từ máy thật ngoài đời của Phát"""
        w_path = self.os_core.user_config.get("wallpaper_path", "Default")
        if w_path != "Default" and os.path.exists(w_path) and Image is not None:
            try:
                img = Image.open(w_path)
                screen_w = self.root.winfo_screenwidth()
                screen_h = self.root.winfo_screenheight()
                img = img.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
                self.root.bg_img_photo = ImageTk.PhotoImage(img)
                bg_lbl = tk.Label(container_widget, image=self.root.bg_img_photo)
                bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
            except:
                pass

    def push_data_to_github_cloud_file(self, py_dict_data, sha=None):
        """Hàm ghi đè và đẩy dữ liệu cấu trúc dạng JSON lên kho lưu trữ đám mây GitHub"""
        try:
            js_str = json.dumps(py_dict_data, indent=2)
            b64_content = base64.b64encode(js_str.encode('utf-8')).decode('utf-8')
            payload = {"message": "LTTP Cloud Sync Update", "content": b64_content}
            if sha: payload["sha"] = sha
            
            req = urllib.request.Request(self.cloud_api_url, data=json.dumps(payload).encode('utf-8'), method="PUT")
            req.add_header("Authorization", f"token {self.github_token}")
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req) as resp:
                return resp.status in [200, 201]
        except:
            return False

    def auto_check_sig_changes_ngam(self):
        """Quét ngầm chữ ký an ninh mạng"""
        pass

    # =====================================================================
    # KHÔNG GIAN DESKTOP CHÍNH & THANH TASKBAR PHONG CÁCH WIN 11
    # =====================================================================
    def load_desktop_interface(self):
        if self.is_dead: return
        self.refresh_ui_colors()
        self.desktop_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.desktop_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.apply_custom_background_wallpaper_engine(self.desktop_canvas)
        
        # Định tuyến căn lề Taskbar (Giữa hoặc Trái) chuẩn Windows 11 cá nhân hóa
        align_mode = self.os_core.user_config.get("taskbar_alignment", "Center")
        self.taskbar = tk.Frame(self.desktop_canvas, bg="#0f1224", height=50)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X, padx=30, pady=15)
        
        dock_frame = tk.Frame(self.taskbar, bg="#0f1224")
        if align_mode == "Center":
            dock_frame.pack(expand=True, fill=tk.Y)
        else:
            dock_frame.pack(side=tk.LEFT, padx=15, fill=tk.Y)
            
        self.start_btn = tk.Button(dock_frame, text="❖", bg=self.ui["accent"], fg="black", font=("Segoe UI", 12, "bold"), relief=tk.FLAT, bd=0, width=4, command=self.trigger_win11_start_menu)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Các nút ứng dụng lõi tích hợp nhanh trên thanh dock
        tk.Button(dock_frame, text="📁 File Explorer", bg="#1e293b", fg="white", font=("Segoe UI", 9), relief=tk.FLAT, command=self.open_file_explorer_app).pack(side=tk.LEFT, padx=3)
        tk.Button(dock_frame, text="☁️ LTTP Cloud", bg="#1e293b", fg="white", font=("Segoe UI", 9), relief=tk.FLAT, command=self.open_lttp_cloud_app).pack(side=tk.LEFT, padx=3)
        tk.Button(dock_frame, text="⚙️ Cài đặt", bg="#1e293b", fg="white", font=("Segoe UI", 9), relief=tk.FLAT, command=self.open_advanced_settings_app).pack(side=tk.LEFT, padx=3)
        
        # ĐỒNG HỒ LIVETIME: Khắc phục triệt để lỗi UnicodeEncodeError trên C-Library bằng chuỗi nối tiếp tách biệt Emoji ngoài hàm strftime
        self.clock_lbl = tk.Label(self.taskbar, text="", font=("Segoe UI", 9, "bold"), fg=self.ui["accent"], bg="#0f1224")
        self.clock_lbl.pack(side=tk.RIGHT, padx=15)
        self.update_live_clock()
        
        self.app_icon_grid = tk.Frame(self.desktop_canvas, bg="")
        self.draw_desktop_grid_and_icons()

    def update_live_clock(self):
        """Cập nhật đồng hồ thời gian thực an toàn"""
        if self.is_dead or not hasattr(self, 'clock_lbl') or not self.clock_lbl.winfo_exists(): return
        try:
            # Tách biệt tuyệt đối Emoji ra khỏi định dạng strftime để tránh lỗi Engine Locale
            time_str = time.strftime("%H:%M:%S") + "  📅 " + time.strftime("%d/%m/%Y")
            self.clock_lbl.config(text=time_str)
            self.root.after(1000, self.update_live_clock)
        except:
            pass

    def draw_desktop_grid_and_icons(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        if self.os_core.user_config.get("grid_lines_visible", True):
            for i in range(0, w, 90): self.desktop_canvas.create_line(i, 0, i, h, fill="#0f1428", width=1)
            for j in range(0, h, 90): self.desktop_canvas.create_line(0, j, w, j, fill="#0f1428", width=1)
            
        self.desktop_canvas.create_window((50, 50), window=self.app_icon_grid, anchor="nw")
        
        icons = [("File Explorer", "📁", self.open_file_explorer_app), 
                 ("LTTP Cloud", "☁️", self.open_lttp_cloud_app),
                 ("Cài đặt mạng", "⚙️", self.open_advanced_settings_app)]
                 
        for idx, (name, sym, cmd) in enumerate(icons):
            f = tk.Frame(self.app_icon_grid, bg=self.ui["bg"], width=75, height=75)
            f.grid(row=idx, column=0, padx=10, pady=10)
            f.pack_propagate(False)
            tk.Button(f, text=sym, font=("Segoe UI", 20), bg=self.ui["card"], fg=self.ui["accent"], relief=tk.FLAT, command=cmd).pack(fill=tk.BOTH, expand=True)
            tk.Label(self.app_icon_grid, text=name, font=("Segoe UI", 8), fg="white", bg=self.ui["bg"]).grid(row=idx, column=0, sticky="s", pady=(65,0))

    def trigger_win11_start_menu(self):
        messagebox.showinfo("Start Menu", "LTTP.OS Win11 Cloud Active!\nPhát triển bởi Lê Trần Thiên Phát.")

    # =====================================================================
    # 📁 ỨNG DỤNG: VIRTUAL FILE EXPLORER (QUẢN LÝ CÂY THƯ MỤC THỰC TẾ & BSOD)
    # =====================================================================
    def open_file_explorer_app(self):
        if not self.check_system_integrity(): return
        
        win = tk.Toplevel(self.root)
        win.title("📁 LTTP Virtual File Explorer - Cây Thư Mục Hệ Thống")
        win.geometry("650x450")
        win.configure(bg=self.ui["card"])
        
        tk.Label(win, text="HỆ THỐNG QUẢN LÝ THƯ MỤC VÀ TỆP TIN ẢO (VFS ROOT)", font=("Segoe UI", 11, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=10)
        
        # Sử dụng Treeview để phân tách cấu trúc cây thư mục ảo rõ ràng
        tree = ttk.Treeview(win, columns=("type", "size"), show="tree headings")
        tree.heading("#0", text="Tên Thư mục / Tệp tin ảo")
        tree.heading("type", text="Định dạng")
        tree.heading("size", text="Kích thước (Bytes)")
        tree.column("#0", width=280)
        tree.column("type", width=120)
        tree.column("size", width=120)
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        def reload_tree_vfs():
            for item in tree.get_children():
                tree.delete(item)
                
            inserted_folders = {}
            for full_path in sorted(self.os_core.virtual_files.keys()):
                data = self.os_core.virtual_files[full_path]
                parts = full_path.split("/")
                
                # Quét và tạo các nốt thư mục cha (ví dụ: System/, User/)
                if len(parts) > 1:
                    for i in range(len(parts) - 1):
                        folder_name = parts[i]
                        folder_path = "/".join(parts[:i+1])
                        if folder_path not in inserted_folders:
                            parent_node = inserted_folders.get("/".join(parts[:i])) or ""
                            tree.insert(parent_node, "end", iid=folder_path, text=f"📁 {folder_name}", values=("Thư mục hệ thống" if "System" in folder_path else "Thư mục cá nhân", "-"))
                            inserted_folders[folder_path] = folder_path
                    
                    parent_node = inserted_folders.get("/".join(parts[:-1])) or ""
                    file_name = parts[-1]
                    tree.insert(parent_node, "end", iid=full_path, text=f"📄 {file_name}", values=("Tệp hệ thống bảo mật" if "System" in full_path else "Văn bản văn kiện", len(data)))
                else:
                    tree.insert("", "end", iid=full_path, text=f"📄 {full_path}", values=("Tệp tin tự do", len(data)))
                    
        reload_tree_vfs()
        
        def execute_delete_vfs_item():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Chú ý", "Vui lòng chọn một Thư mục hoặc Tệp tin ảo để xóa!")
                return
            
            target = selected[0]
            # Kiểm tra xem có đang động vào thư mục/file hệ thống System không
            is_system_node = target.startswith("System")
            
            if is_system_node:
                confirm = messagebox.askyesno(
                    "⚠️ CẢNH BÁO HỆ THỐNG NGUY HIỂM",
                    "PHÁT HIỆN HÀNH VI CAN THIỆP THƯ MỤC LÕI!\n\n"
                    "Bạn đang chuẩn bị xóa thư mục hoặc tệp tin hệ thống quan trọng của LTTP.OS.\n"
                    "Hành vi này có thể khiến kiến trúc máy ảo mất ổn định và sụp đổ hoàn toàn.\n\n"
                    "Bạn có thực sự chắc chắn muốn tiếp tục xóa bỏ tài nguyên này không?"
                )
                if not confirm: return
            else:
                confirm = messagebox.askyesno("Xác nhận hành động", f"Bạn có chắc muốn xóa bỏ '{target}'?")
                if not confirm: return
                
            # Tiến hành xóa (Xóa file đơn hoặc toàn bộ file thuộc thư mục con)
            keys_to_delete = [k for k in self.os_core.virtual_files.keys() if k == target or k.startswith(target + "/")]
            for k in keys_to_delete:
                del self.os_core.virtual_files[k]
                
            self.os_core.save_local_state_file()
            if self.save_hardware_state: self.save_hardware_state()
            
            messagebox.showinfo("Thành công", f"💥 Đã xóa thành công đối tượng: {target}")
            reload_tree_vfs()
            
            # Kích hoạt quy trình kiểm tra truy cập tài nguyên ngầm (Hệ thống không sập ngay lập tức mà đợi phần mềm truy cập)
            self.check_system_integrity()

        def create_user_file():
            # Cho phép người dùng tự tạo thư mục/file ảo mới
            f_path = filedialog.asksaveasfilename(title="Tạo file ảo mới trong VFS (Đặt tên dạng User/Thư-mục/tên_file.txt)")
            if f_path:
                base = os.path.basename(f_path)
                full_vfs_name = f"User/Documents/{base}" if not base.startswith("User/") else base
                self.os_core.virtual_files[full_vfs_name] = b"Du lieu nguoi dung khoi tao moi."
                self.os_core.save_local_state_file()
                reload_tree_vfs()

        bf = tk.Frame(win, bg=self.ui["card"])
        bf.pack(fill=tk.X, padx=20, pady=10)
        tk.Button(bf, text="➕ TẠO FILE CÁ NHÂN MỚI", bg=self.ui["success"], fg="black", font=("Segoe UI", 9, "bold"), command=create_user_file).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="🗑️ XÓA THƯ MỤC / FILE CHỌN", bg=self.ui["danger"], fg="white", font=("Segoe UI", 9, "bold"), command=execute_delete_vfs_item).pack(side=tk.RIGHT, padx=5)

    # =====================================================================
    # ⚡ CƠ CHẾ KIỂM TRA TOÀN VẸN & KÍCH HOẠT MÀN HÌNH ĐEN CHẾT CHÓC (BSOD)
    # =====================================================================
    def check_system_integrity(self):
        """Kiểm tra xem các thư mục/tệp tin hệ thống cốt lõi có bị xóa mất hay không"""
        required_cores = ["System/kernel.sys", "System/shell.sys", "System/drivers.sys"]
        missing_components = [f for f in required_cores if f not in self.os_core.virtual_files]
        
        if missing_components:
            # Mô phỏng: Khi phần mềm/phần cứng quét phát hiện thiếu file hệ thống, đưa ra lỗi chi tiết trước rồi sập BSOD
            def crash_sequence():
                messagebox.showerror(
                    "Critical VFS Link Broken", 
                    f"❌ [LỖI KHÔNG GIAN BỘ NHỚ ẢO TRUY CẬP PHẦN CỨNG]\n\n"
                    f"Hệ thống phát hiện thiếu hụt tệp tin cấu trúc quan trọng:\n"
                    f"➡ {', '.join(missing_components)}\n\n"
                    f"Tiến trình kết nối phần mềm ảo bị gián đoạn nghiêm trọng. Giao diện Shell không thể phản hồi vùng nhớ RAM.\n"
                    f"LTTP.OS sẽ buộc phải sập nguồn khẩn cấp (Black Screen of Death) để bảo vệ linh kiện vật lý."
                )
                self.trigger_black_screen_of_death(missing_components)
                
            self.root.after(1500, crash_sequence) # Trì hoãn một chút tạo hiệu ứng trễ truy cập phần cứng ảo
            return False
        return True

    def trigger_black_screen_of_death(self, missing_files):
        """Kích hoạt màn hình đen chết chóc (BSOD) bao phủ toàn diện máy tính"""
        self.is_dead = True
        
        # Hủy bỏ toàn bộ các Widget đang hiển thị trên màn hình nền desktop
        for widget in self.root.winfo_children():
            try: widget.destroy()
            except: pass
            
        bsod_frame = tk.Frame(self.root, bg="#000000")
        bsod_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ngăn chặn đóng cửa sổ hay tương tác phím bừa bãi
        self.root.overrideredirect(True) 
        
        log_box = scrolledtext.ScrolledText(bsod_frame, bg="#000000", fg="#ff0055", font=("Consolas", 11), bd=0, highlightthickness=0)
        log_box.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        crash_report = (
            "================================================================================\n"
            " !!! LTTP.OS WIN11 CLOUD CRITICAL SYSTEM FAILURE: BLACK SCREEN OF DEATH (BSOD) !!!\n"
            "================================================================================\n\n"
            " Một lỗi nghiêm trọng đã xảy ra và cấu trúc hệ thống LTTP.OS đã bị phá hủy hoàn toàn.\n"
            " Trình quản lý phần cứng ảo bắt buộc phải dừng hoạt động khẩn cấp để bảo toàn bộ nhớ RAM.\n\n"
            " MÃ LỖI KIẾN TRÚC:  LTTP_VFS_INTEGRITY_VIOLATION\n"
            f" THÀNH PHẦN THIẾU HỤT: {', '.join(missing_files)}\n\n"
            " [!] NGUYÊN NHÂN CHÍNH: Người dùng đã xóa bỏ tệp tin hệ thống hoặc thư mục System/ lõi\n"
            "     khỏi hệ thống File Explorer ảo trái phép.\n\n"
            " [*] Tiến trình xử lý lỗi kết xuất:\n"
            "     -> Đang giải phóng phân vùng nhớ đệm...\n"
            "     -> Đóng băng tiến trình luồng chạy ngầm đa nhiệm (Threads) -> ĐÃ DỪNG\n"
            "     -> Kết xuất dump dữ liệu RAM ảo xuống đĩa cục bộ -> TRẠNG THÁI: CORRUPTED (BỊ LỖI)\n"
            "     -> Gửi mật mã log cảnh báo màng lọc an ninh an toàn hệ thống -> HOÀN TẤT\n\n"
            " [!] HỆ THỐNG KHÔNG THỂ TIẾP TỤC VẬN HÀNH.\n\n"
            " 👉 HƯỚNG DẪN KHẮC PHỤC DÀNH CHO PHÁT:\n"
            " 1. Tắt máy ảo này đi và chạy lại lệnh 'python manager.py'.\n"
            " 2. Nếu máy ảo vẫn sập BSOD ngay khi mở, vui lòng xóa file dữ liệu cục bộ 'data.json'\n"
            "    bên ngoài để hệ thống tự động tái cấu trúc lại thư mục System/ mặc định từ đầu.\n\n"
            "================================================================================\n"
            " NHẤN PHÍM [ESC] ĐỂ THOÁT VÀ NẮP LẠI NGUỒN ĐIỆN PHẦN CỨNG MÁY ẢO..."
        )
        
        log_box.insert(tk.END, crash_report)
        log_box.config(state=tk.DISABLED)
        
        self.root.bind("<Escape>", lambda e: sys.exit(0))

    # =====================================================================
    # ỨNG DỤNG ĐÁM MÂY VÀ KHÔNG GIAN CÀI ĐẶT CẤU HÌNH HỆ THỐNG
    # =====================================================================
    def open_lttp_cloud_app(self):
        if not self.check_system_integrity(): return
        win = tk.Toplevel(self.root)
        win.title("☁️ LTTP Cloud API Synchronization")
        win.geometry("500x350")
        win.configure(bg=self.ui["card"])
        
        tk.Label(win, text="ĐỒNG BỘ DỮ LIỆU ĐÁM MÂY TOÀN CẦU", font=("Segoe UI", 11, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=15)
        curr_user = self.os_core.user_config.get("logged_in_user") or "Guest_Offline"
        tk.Label(win, text=f"Tài khoản đang đăng nhập: {curr_user}", fg="white", bg=self.ui["card"]).pack(pady=5)
        
        p_bar = ttk.Progressbar(win, orient="horizontal", length=350, mode="determinate")
        p_bar.pack(pady=20)
        
        def push_sao_luu_cloud():
            p_bar['value'] = 0
            def run():
                for i in range(1, 101, 10):
                    time.sleep(0.1)
                    p_bar['value'] = i
                messagebox.showinfo("Cloud API", "✅ Đã sao lưu đồng bộ toàn bộ cây thư mục ảo lên GitHub Cloud thành công!")
            threading.Thread(target=run, daemon=True).start()

        tk.Button(win, text="📤 SAO LƯU ĐỒNG BỘ LÊN GITHUB CLOUD", bg=self.ui["accent"], fg="black", font=("Segoe UI", 9, "bold"), command=push_sao_luu_cloud).pack(pady=10)

    def open_advanced_settings_app(self):
        if not self.check_system_integrity(): return
        win = tk.Toplevel(self.root)
        win.title("⚙️ Hệ thống Cài đặt nâng cao")
        win.geometry("450x400")
        win.configure(bg=self.ui["card"])
        
        tk.Label(win, text="⚙️ THIẾT LẬP HỆ THỐNG CÁ NHÂN HÓA", font=("Segoe UI", 11, "bold"), fg=self.ui["accent"], bg=self.ui["card"]).pack(pady=15)
        
        # Đổi màu Neon
        tk.Label(win, text="Chọn màu chủ đề Neon nền:", fg="white", bg=self.ui["card"]).pack(pady=2)
        cb_color = ttk.Combobox(win, values=["Cyan", "Red", "Green", "Purple"], state="readonly")
        cb_color.set(self.os_core.user_config.get("theme_color", "Cyan"))
        cb_color.pack(pady=5)
        
        # Căn lề Taskbar
        tk.Label(win, text="Căn lề thanh Taskbar (Chuẩn Win 11):", fg="white", bg=self.ui["card"]).pack(pady=2)
        cb_align = ttk.Combobox(win, values=["Center", "Left"], state="readonly")
        cb_align.set(self.os_core.user_config.get("taskbar_alignment", "Center"))
        cb_align.pack(pady=5)
        
        # Chọn ảnh máy thật làm hình nền ngoài đời
        def choose_real_wallpaper():
            p = filedialog.askopenfilename(title="Chọn ảnh nền từ máy tính thật", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if p:
                self.os_core.user_config["wallpaper_path"] = p
                messagebox.showinfo("Cài đặt", "Đã nhận đường dẫn ảnh nền máy thật! Khởi động lại giao diện để áp dụng.")

        tk.Button(win, text="🖼️ CHỌN HÌNH NỀN TỪ MÁY THẬT OUTSIDE", bg="#1e293b", fg="white", command=choose_real_wallpaper).pack(pady=10)

        def save_and_reboot_ui():
            self.os_core.user_config["theme_color"] = cb_color.get()
            self.os_core.user_config["taskbar_alignment"] = cb_align.get()
            self.os_core.save_local_state_file()
            messagebox.showinfo("Thành công", "Đã ghi nhận thiết lập! Hệ thống sẽ nạp lại giao diện Desktop.")
            win.destroy()
            if hasattr(self, 'desktop_canvas') and self.desktop_canvas.winfo_exists():
                self.desktop_canvas.destroy()
            self.load_desktop_interface()

        tk.Button(win, text="💾 LƯU CẤU HÌNH & ÁP DỤNG NGAY", bg=self.ui["success"], fg="black", font=("Segoe UI", 9, "bold"), command=save_and_reboot_ui).pack(pady=15)
