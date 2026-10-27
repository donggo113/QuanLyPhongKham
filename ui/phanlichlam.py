# ui/phanlichlam.py
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from utils import log_action


class ShiftManagementView(tk.Frame):

    def __init__(self, parent, username="admin", role="admin"):
        super().__init__(parent, bg="#FFFFFF")
        self.username = username
        self.role = role
        self.db_file = os.path.join("db", "data_lichlam.json")
        self.data_shifts = []

        self.setup_ui()
        self.load_shifts()

    def setup_ui(self):
        header = tk.Frame(self, bg="#FFFFFF")
        header.pack(fill="x", pady=(0, 10))

        role_title = (
            "XẾP LỊCH LÀM VIỆC (QUẢN TRỊ)"
            if str(self.role).lower() == "admin"
            else "ĐĂNG KÝ LỊCH LÀM VIỆC"
        )
        tk.Label(
            header,
            text=f"📅 {role_title}",
            bg="#FFFFFF",
            fg="#EAB308",
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")

        # Khung Đăng ký
        box_reg = tk.LabelFrame(
            self,
            text=" Đăng ký ca làm ",
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 9, "bold"),
            bd=1,
            relief="solid",
        )
        box_reg.pack(fill="x", pady=(0, 10), ipadx=10, ipady=5)

        grid_r = tk.Frame(box_reg, bg="#FFFFFF")
        grid_r.pack(fill="x", padx=10, pady=5)

        tk.Label(
            grid_r,
            text="Mã NV/Tên:",
            bg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.ent_user = ttk.Entry(grid_r, width=20)
        self.ent_user.insert(0, self.username)
        self.ent_user.grid(row=0, column=1, sticky="w", padx=(0, 20))

        tk.Label(
            grid_r,
            text="Ngày làm (YYYY-MM-DD):",
            bg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.ent_ngay = ttk.Entry(grid_r, width=20)
        self.ent_ngay.insert(0, "2026-10-28")
        self.ent_ngay.grid(row=0, column=3, sticky="w", padx=(0, 20))

        tk.Label(
            grid_r, text="Ca làm:", bg="#FFFFFF", font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=4, sticky="w", padx=(0, 5))
        self.cbo_ca = ttk.Combobox(
            grid_r,
            values=[
                "Sáng (07:30 - 11:30)",
                "Chiều (13:30 - 17:30)",
                "Tối (17:30 - 21:00)",
            ],
            state="readonly",
            width=22,
        )
        self.cbo_ca.set("Sáng (07:30 - 11:30)")
        self.cbo_ca.grid(row=0, column=5, sticky="w", padx=(0, 15))

        btn_dk = tk.Button(
            grid_r,
            text="📝 Đăng ký ca",
            command=self.register_shift,
            bg="#EAB308",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
        )
        btn_dk.grid(row=0, column=6)

        # Bảng Treeview
        table_frame = tk.Frame(self, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("MaNV", "Ngay", "CaLam", "TrangThai"),
            show="headings",
        )
        self.tree.heading("MaNV", text="Mã NV")
        self.tree.heading("Ngay", text="Ngày")
        self.tree.heading("CaLam", text="Ca Làm")
        self.tree.heading("TrangThai", text="Trạng Thái")

        self.tree.column("MaNV", anchor="center", width=120)
        self.tree.column("Ngay", anchor="center", width=120)
        self.tree.column("CaLam", anchor="w", width=250)
        self.tree.column("TrangThai", anchor="center", width=120)

        self.tree.pack(fill="both", expand=True)

        # Thanh nút Duyệt dành riêng cho Admin
        if str(self.role).lower() == "admin":
            btn_box = tk.Frame(self, bg="#FFFFFF")
            btn_box.pack(anchor="w")

            tk.Button(
                btn_box,
                text="✅ Duyệt ca chọn",
                command=lambda: self.change_status("Đã duyệt"),
                bg="#22C55E",
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
                bd=0,
                padx=10,
                pady=4,
                cursor="hand2",
            ).pack(side="left", padx=(0, 8))

            tk.Button(
                btn_box,
                text="❌ Từ chối ca chọn",
                command=lambda: self.change_status("Từ chối"),
                bg="#EF4444",
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
                bd=0,
                padx=10,
                pady=4,
                cursor="hand2",
            ).pack(side="left")

    def load_shifts(self):
        self.tree.delete(*self.tree.get_children())
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    self.data_shifts = json.load(f)
            except Exception:
                self.data_shifts = []

        # Đã loại bỏ bản ghi mẫu của 'bacti'
        if not self.data_shifts:
            self.data_shifts = [
                {
                    "MaNV": "admin",
                    "Ngay": "2026-10-28",
                    "CaLam": "Chiều (13:30 - 17:30)",
                    "TrangThai": "Đã duyệt",
                },
            ]
            self.save_shifts()

        for item in self.data_shifts:
            self.tree.insert(
                "",
                "end",
                values=(
                    item["MaNV"],
                    item["Ngay"],
                    item["CaLam"],
                    item["TrangThai"],
                ),
            )

    def save_shifts(self):
        try:
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(self.data_shifts, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def register_shift(self):
        u = self.ent_user.get().strip()
        n = self.ent_ngay.get().strip()
        c = self.cbo_ca.get()

        if not u or not n:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ tên và ngày làm!")
            return

        new_item = {"MaNV": u, "Ngay": n, "CaLam": c, "TrangThai": "Chờ duyệt"}
        self.data_shifts.append(new_item)
        self.save_shifts()
        log_action(self.username, f"Đăng ký ca làm {c} ngày {n}")

        messagebox.showinfo("Thành công", f"Đã đăng ký ca làm thành công cho {u}!")
        self.load_shifts()

    def change_status(self, status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ca làm cần xử lý!")
            return

        idx = self.tree.index(selected[0])
        self.data_shifts[idx]["TrangThai"] = status
        self.save_shifts()
        log_action(self.username, f"Admin chuyển trạng thái ca làm sang '{status}'")

        messagebox.showinfo("Thành công", f"Đã cập nhật trạng thái ca làm thành: {status}")
        self.load_shifts()