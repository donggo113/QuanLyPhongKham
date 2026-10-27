# ui/dangkylichkham.py
import csv
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from utils import log_action


class AppointmentRegistrationView(tk.Frame):

    def __init__(self, parent, role="admin"):
        super().__init__(parent, bg="#FFFFFF")
        self.role = role
        self.file_appointments = os.path.join("db", "data_lichkham.json")
        self.file_benhnhan = os.path.join("db", "data_phongkham.json")
        self.file_bacsi = os.path.join("db", "data_bacsi.json")

        self.setup_ui()
        self.load_combobox_data()
        self.load_appointments()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#FFFFFF")
        header.pack(fill="x", pady=(0, 10))

        tk.Label(
            header,
            text="📅 Đăng Ký & Đặt Lịch Khám",
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 15, "bold"),
        ).pack(side="left")

        # Khung Đặt Lịch
        box_form = tk.LabelFrame(
            self,
            text=" Thêm Lịch Hẹn Mới ",
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 9, "bold"),
            bd=1,
            relief="solid",
        )
        box_form.pack(fill="x", pady=(0, 10), ipadx=10, ipady=5)

        grid_f = tk.Frame(box_form, bg="#FFFFFF")
        grid_f.pack(fill="x", padx=10, pady=5)

        tk.Label(
            grid_f, text="Bệnh nhân:", bg="#FFFFFF", font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.cbo_benh_nhan = ttk.Combobox(grid_f, width=32, state="readonly")
        self.cbo_benh_nhan.grid(row=0, column=1, sticky="w", padx=(0, 20))

        tk.Label(
            grid_f, text="Bác sĩ khám:", bg="#FFFFFF", font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.cbo_bac_si = ttk.Combobox(grid_f, width=35, state="readonly")
        self.cbo_bac_si.grid(row=0, column=3, sticky="w")

        tk.Label(
            grid_f,
            text="Ngày (YYYY-MM-DD):",
            bg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(8, 0))
        self.ent_ngay = ttk.Entry(grid_f, width=35)
        self.ent_ngay.insert(0, "2026-10-27")
        self.ent_ngay.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=(8, 0))

        tk.Label(
            grid_f, text="Giờ khám:", bg="#FFFFFF", font=("Segoe UI", 9, "bold")
        ).grid(row=1, column=2, sticky="w", padx=(0, 5), pady=(8, 0))
        self.cbo_gio = ttk.Combobox(
            grid_f,
            values=[
                "08:00",
                "09:00",
                "10:00",
                "11:00",
                "14:00",
                "15:00",
                "16:00",
            ],
            state="readonly",
            width=15,
        )
        self.cbo_gio.set("09:00")
        self.cbo_gio.grid(row=1, column=3, sticky="w", pady=(8, 0))

        btn_dat = tk.Button(
            grid_f,
            text="➕ Đặt Lịch",
            command=self.create_appointment,
            bg="#EAB308",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=12,
            pady=3,
            cursor="hand2",
        )
        btn_dat.grid(row=1, column=4, padx=(15, 0), pady=(8, 0))

        # Nút Xuất Báo Cáo
        btn_csv = tk.Button(
            self,
            text="📄 Xuất Báo Cáo Lịch Hẹn (CSV)",
            command=self.export_csv,
            bg="#FEF08A",
            fg="#854D0E",
            font=("Segoe UI", 9, "bold"),
            bd=1,
            relief="solid",
            padx=8,
            pady=3,
            cursor="hand2",
        )
        btn_csv.pack(anchor="w", pady=(0, 5))

        # Bảng hiển thị danh sách
        table_frame = tk.Frame(self, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("MaBS", "BacSi", "BenhNhan", "NgayKham", "GioKham"),
            show="headings",
        )
        self.tree.heading("MaBS", text="Mã BS")
        self.tree.heading("BacSi", text="Bác Sĩ Khám")
        self.tree.heading("BenhNhan", text="Bệnh Nhân")
        self.tree.heading("NgayKham", text="Ngày Khám")
        self.tree.heading("GioKham", text="Giờ Khám")

        self.tree.column("MaBS", anchor="center", width=80)
        self.tree.column("BacSi", anchor="w", width=200)
        self.tree.column("BenhNhan", anchor="w", width=200)
        self.tree.column("NgayKham", anchor="center", width=110)
        self.tree.column("GioKham", anchor="center", width=90)

        self.tree.pack(fill="both", expand=True)

    def load_combobox_data(self):
        """Đọc danh sách Bệnh Nhân và Bác Sĩ thực tế từ JSON"""
        # Bệnh nhân
        list_bn = []
        if os.path.exists(self.file_benhnhan):
            try:
                with open(self.file_benhnhan, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        list_bn.append(f"{item['MaBN']} - {item['HoTen']}")
            except Exception:
                pass
        if not list_bn:
            list_bn = ["BN001 - Nguyễn Văn An", "BN002 - Trần Thị Bích"]
        self.cbo_benh_nhan["values"] = list_bn
        self.cbo_benh_nhan.set(list_bn[0])

        # Bác sĩ
        list_bs = []
        if os.path.exists(self.file_bacsi):
            try:
                with open(self.file_bacsi, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        list_bs.append(f"{item['MaBS']} - {item['HoTen']}")
            except Exception:
                pass
        if not list_bs:
            list_bs = [
                "BS001 - PGS.TS Nguyễn Văn Bình",
                "BS002 - ThS.BS Trần Thị Mai",
            ]
        self.cbo_bac_si["values"] = list_bs
        self.cbo_bac_si.set(list_bs[0])

    def load_appointments(self):
        """Hiển thị danh sách lịch hẹn từ file"""
        self.tree.delete(*self.tree.get_children())
        data_appointments = []

        if os.path.exists(self.file_appointments):
            try:
                with open(self.file_appointments, "r", encoding="utf-8") as f:
                    data_appointments = json.load(f)
            except Exception:
                pass

        if not data_appointments:
            data_appointments = [
                {
                    "MaBS": "BS001",
                    "BacSi": "PGS.TS Nguyễn Văn Bình",
                    "BenhNhan": "Nguyễn Văn An",
                    "NgayKham": "2026-10-27",
                    "GioKham": "09:00",
                },
                {
                    "MaBS": "BS002",
                    "BacSi": "ThS.BS Trần Thị Mai",
                    "BenhNhan": "Trần Thị Bích",
                    "NgayKham": "2026-10-27",
                    "GioKham": "10:00",
                },
            ]
            self.save_appointments(data_appointments)

        for item in data_appointments:
            self.tree.insert(
                "",
                "end",
                values=(
                    item["MaBS"],
                    item["BacSi"],
                    item["BenhNhan"],
                    item["NgayKham"],
                    item.get("GioKham", "09:00"),
                ),
            )

    def save_appointments(self, data):
        try:
            os.makedirs(os.path.dirname(self.file_appointments), exist_ok=True)
            with open(self.file_appointments, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def create_appointment(self):
        bn = self.cbo_benh_nhan.get()
        bs = self.cbo_bac_si.get()
        ngay = self.ent_ngay.get().strip()
        gio = self.cbo_gio.get()

        if not ngay:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ngày khám!")
            return

        ma_bs = bs.split(" - ")[0]
        ten_bs = bs.split(" - ")[1] if " - " in bs else bs
        ten_bn = bn.split(" - ")[1] if " - " in bn else bn

        data = []
        if os.path.exists(self.file_appointments):
            try:
                with open(self.file_appointments, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass

        new_item = {
            "MaBS": ma_bs,
            "BacSi": ten_bs,
            "BenhNhan": ten_bn,
            "NgayKham": ngay,
            "GioKham": gio,
        }
        data.append(new_item)
        self.save_appointments(data)
        log_action(self.role, f"Đặt lịch khám mới cho bệnh nhân {ten_bn} với {ten_bs}")

        messagebox.showinfo("Thành công", f"Đã đặt lịch thành công cho bệnh nhân {ten_bn}!")
        self.load_appointments()

    def export_csv(self):
        """Xuất báo cáo CSV chuẩn lề và tự động chống lỗi ##### trong Excel"""
        csv_file = os.path.join("db", "bao_cao_lich_kham.csv")
        try:
            with open(
                csv_file, "w", newline="", encoding="utf-8-sig"
            ) as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(
                    [
                        "Mã BS",
                        "Bác Sĩ Khám",
                        "Bệnh Nhân",
                        "Ngày Khám",
                        "Giờ Khám",
                    ]
                )
                for child in self.tree.get_children():
                    vals = list(self.tree.item(child, "values"))
                    vals[3] = f"'{vals[3]}"
                    writer.writerow(vals)
            messagebox.showinfo(
                "Thành công",
                f"Đã xuất báo cáo CSV chia cột chuẩn: {csv_file}",
            )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất CSV: {e}")