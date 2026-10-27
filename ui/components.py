# ui/components.py
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from utils import log_action, validate_phone


class DataView(tk.Frame):

    def __init__(self, parent, role="admin"):
        super().__init__(parent, bg="#FFFFFF")
        self.role = role
        self.db_file = os.path.join("db", "data_phongkham.json")
        self.data_list = []

        self.setup_ui()
        self.load_data_from_json()

    def setup_ui(self):
        # Header - Đã loại bỏ chuỗi (Quyền: ...)
        header = tk.Frame(self, bg="#FFFFFF")
        header.pack(fill="x", pady=(0, 10))

        tk.Label(
            header,
            text="👤 QUẢN LÝ HỒ SƠ BỆNH NHÂN",
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")

        # 1. KHUNG TÌM KIẾM & LỌC DỮ LIỆU
        search_frame = tk.LabelFrame(
            self,
            text=" Tìm kiếm & Lọc dữ liệu ",
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 9, "bold"),
            bd=1,
            relief="solid",
        )
        search_frame.pack(fill="x", pady=(0, 10), ipadx=10, ipady=5)

        tk.Label(
            search_frame, text="Tìm kiếm:", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=0, column=0, padx=5, pady=5)
        self.ent_search = ttk.Entry(search_frame, width=25)
        self.ent_search.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            search_frame,
            text="Tiêu chí:",
            bg="#FFFFFF",
            font=("Segoe UI", 9),
        ).grid(row=0, column=2, padx=5, pady=5)
        self.cbo_criterion = ttk.Combobox(
            search_frame,
            values=["Mã BN / Tên", "Số điện thoại"],
            state="readonly",
            width=15,
        )
        self.cbo_criterion.set("Mã BN / Tên")
        self.cbo_criterion.grid(row=0, column=3, padx=5, pady=5)

        btn_search = tk.Button(
            search_frame,
            text="🔍 Tìm kiếm",
            command=self.search_data,
            bg="#FEF08A",
            fg="#854D0E",
            font=("Segoe UI", 9, "bold"),
            bd=1,
            relief="solid",
            cursor="hand2",
        )
        btn_search.grid(row=0, column=4, padx=5, pady=5)

        btn_refresh = tk.Button(
            search_frame,
            text="🔄 Làm mới",
            command=self.load_data_from_json,
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 9),
            bd=1,
            relief="solid",
            cursor="hand2",
        )
        btn_refresh.grid(row=0, column=5, padx=5, pady=5)

        # 2. KHUNG BẢNG TREEVIEW
        table_frame = tk.Frame(self, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("MaBN", "HoTen", "SoDienThoai", "GioiTinh", "DiaChi")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=8
        )

        self.tree.heading("MaBN", text="Mã BN")
        self.tree.heading("HoTen", text="Họ và Tên")
        self.tree.heading("SoDienThoai", text="Số Điện Thoại")
        self.tree.heading("GioiTinh", text="Giới Tính")
        self.tree.heading("DiaChi", text="Địa Chỉ")

        self.tree.column("MaBN", anchor="center", width=80)
        self.tree.column("HoTen", anchor="w", width=180)
        self.tree.column("SoDienThoai", anchor="center", width=120)
        self.tree.column("GioiTinh", anchor="center", width=90)
        self.tree.column("DiaChi", anchor="w", width=250)

        self.tree.pack(fill="both", expand=True, side="left")
        self.tree.bind("<<TreeviewSelect>>", self.on_select_record)

        # 3. KHUNG FORM NHẬP LIỆU
        form_frame = tk.LabelFrame(
            self,
            text=" Thông tin bệnh nhân ",
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 9, "bold"),
            bd=1,
            relief="solid",
        )
        form_frame.pack(fill="x", ipadx=10, ipady=5)

        # Hàng 0: Mã BN + Họ và Tên
        tk.Label(
            form_frame, text="Mã Bệnh Nhân:*", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.ent_mabn = ttk.Entry(form_frame, width=20)
        self.ent_mabn.grid(row=0, column=1, sticky="w", padx=5, pady=3)

        tk.Label(
            form_frame, text="Họ và Tên:*", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.ent_hoten = ttk.Entry(form_frame, width=35)
        self.ent_hoten.grid(row=0, column=3, sticky="w", padx=5, pady=3)

        # Hàng 1: Số Điện Thoại + Giới Tính
        tk.Label(
            form_frame,
            text="Số Điện Thoại:*",
            bg="#FFFFFF",
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.ent_sdt = ttk.Entry(form_frame, width=20)
        self.ent_sdt.grid(row=1, column=1, sticky="w", padx=5, pady=3)

        tk.Label(
            form_frame, text="Giới Tính:", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=1, column=2, sticky="w", padx=5, pady=3)
        self.cbo_gioitinh = ttk.Combobox(
            form_frame, values=["Nam", "Nữ", "Khác"], state="readonly", width=12
        )
        self.cbo_gioitinh.set("Nam")
        self.cbo_gioitinh.grid(row=1, column=3, sticky="w", padx=5, pady=3)

        # Hàng 2: Ô Địa Chỉ
        tk.Label(
            form_frame, text="Địa Chỉ:", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.ent_diachi = ttk.Entry(form_frame, width=65)
        self.ent_diachi.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=3)

        # Thanh chứa các nút bấm
        btn_box = tk.Frame(form_frame, bg="#FFFFFF")
        btn_box.grid(row=3, column=0, columnspan=4, pady=8, sticky="e")

        tk.Button(
            btn_box,
            text="🧹 Nhập lại",
            command=self.clear_form,
            bg="#F3F4F6",
            fg="#1F2937",
            font=("Segoe UI", 9),
            bd=1,
            relief="solid",
            padx=8,
            pady=2,
            cursor="hand2",
        ).pack(side="left", padx=5)

        tk.Button(
            btn_box,
            text="➕ Thêm mới",
            command=self.create_record,
            bg="#EAB308",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
        ).pack(side="left", padx=5)

        tk.Button(
            btn_box,
            text="✏️ Cập nhật",
            command=self.update_record,
            bg="#3B82F6",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
        ).pack(side="left", padx=5)

        if str(self.role).lower() == "admin":
            tk.Button(
                btn_box,
                text="🗑️ Xóa",
                command=self.delete_record,
                bg="#EF4444",
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
                bd=0,
                padx=10,
                pady=3,
                cursor="hand2",
            ).pack(side="left", padx=5)

    def load_data_from_json(self):
        """Đọc và hiển thị dữ liệu từ file JSON"""
        self.tree.delete(*self.tree.get_children())
        self.data_list.clear()

        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)

                if isinstance(raw_data, dict):
                    raw_list = raw_data.get("danh_sach_benh_nhan", [])
                elif isinstance(raw_data, list):
                    raw_list = raw_data
                else:
                    raw_list = []

                for item in raw_list:
                    if isinstance(item, dict):
                        mabn = item.get("MaBN") or item.get("ma_id") or "BN000"
                        hoten = item.get("HoTen") or item.get("ho_ten") or ""
                        sdt = item.get("SoDienThoai") or item.get("sdt") or ""
                        gt = item.get("GioiTinh") or item.get("gioi_tinh") or "Nam"
                        diachi = item.get("DiaChi") or item.get("dia_chi") or "Chưa cập nhật"

                        self.data_list.append(
                            {
                                "MaBN": mabn,
                                "HoTen": hoten,
                                "SoDienThoai": sdt,
                                "GioiTinh": gt,
                                "DiaChi": diachi,
                            }
                        )
            except Exception as e:
                print("Lỗi đọc file JSON Bệnh nhân:", e)
                self.data_list = []

        if not self.data_list:
            self.data_list = [
                {
                    "MaBN": "BN001",
                    "HoTen": "Nguyễn Văn An",
                    "SoDienThoai": "0912345678",
                    "GioiTinh": "Nam",
                    "DiaChi": "Hà Nội",
                },
                {
                    "MaBN": "BN002",
                    "HoTen": "Trần Thị Bích",
                    "SoDienThoai": "0987654321",
                    "GioiTinh": "Nữ",
                    "DiaChi": "TP.HCM",
                },
            ]
            self.save_data_to_json()

        for item in self.data_list:
            self.tree.insert(
                "",
                "end",
                values=(
                    item["MaBN"],
                    item["HoTen"],
                    item["SoDienThoai"],
                    item["GioiTinh"],
                    item["DiaChi"],
                ),
            )
        self.clear_form()

    def save_data_to_json(self):
        """Ghi dữ liệu danh sách bệnh nhân trở lại file JSON"""
        try:
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(self.data_list, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            messagebox.showerror(
                "Lỗi Lưu File", f"Không thể lưu file JSON: {e}", parent=self
            )
            return False

    def create_record(self):
        """Thêm mới bệnh nhân"""
        ma = self.ent_mabn.get().strip().upper()
        ten = self.ent_hoten.get().strip()
        sdt = self.ent_sdt.get().strip()
        gt = self.cbo_gioitinh.get()
        diachi = self.ent_diachi.get().strip() or "Chưa cập nhật"

        if not ma or not ten or not sdt:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng nhập đầy đủ các trường bắt buộc (*)",
                parent=self,
            )
            return

        if any(item["MaBN"] == ma for item in self.data_list):
            messagebox.showerror(
                "Lỗi trùng mã", f"Mã bệnh nhân '{ma}' đã tồn tại!", parent=self
            )
            return

        if not validate_phone(sdt):
            messagebox.showerror(
                "Lỗi định dạng",
                "Số điện thoại không hợp lệ (Phải đúng 10 số bắt đầu bằng 0)!",
                parent=self,
            )
            return

        new_item = {
            "MaBN": ma,
            "HoTen": ten,
            "SoDienThoai": sdt,
            "GioiTinh": gt,
            "DiaChi": diachi,
        }
        self.data_list.append(new_item)

        if self.save_data_to_json():
            log_action(self.role, f"Thêm mới bệnh nhân thành công: {ma} - {ten}")
            messagebox.showinfo(
                "Thành công", f"Đã thêm bệnh nhân {ma} thành công!", parent=self
            )
            self.load_data_from_json()

    def update_record(self):
        """Cập nhật thông tin bệnh nhân"""
        ma = self.ent_mabn.get().strip().upper()
        ten = self.ent_hoten.get().strip()
        sdt = self.ent_sdt.get().strip()
        gt = self.cbo_gioitinh.get()
        diachi = self.ent_diachi.get().strip() or "Chưa cập nhật"

        if not ma:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng chọn một bệnh nhân từ bảng để chỉnh sửa!",
                parent=self,
            )
            return

        if not validate_phone(sdt):
            messagebox.showerror(
                "Lỗi định dạng", "Số điện thoại không hợp lệ!", parent=self
            )
            return

        found = False
        for item in self.data_list:
            if item["MaBN"] == ma:
                item["HoTen"] = ten
                item["SoDienThoai"] = sdt
                item["GioiTinh"] = gt
                item["DiaChi"] = diachi
                found = True
                break

        if found and self.save_data_to_json():
            log_action(self.role, f"Cập nhật thông tin bệnh nhân: {ma}")
            messagebox.showinfo(
                "Thành công",
                f"Đã cập nhật dữ liệu bệnh nhân {ma}!",
                parent=self,
            )
            self.load_data_from_json()

    def delete_record(self):
        """Xóa bệnh nhân khỏi hệ thống"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Cảnh báo", "Vui lòng chọn bệnh nhân cần xóa!", parent=self
            )
            return

        vals = self.tree.item(selected[0], "values")
        ma = vals[0]
        ten = vals[1]

        if messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa bệnh nhân '{ten}' ({ma}) không?",
            parent=self,
        ):
            self.data_list = [
                item for item in self.data_list if item["MaBN"] != ma
            ]
            if self.save_data_to_json():
                log_action(self.role, f"Xóa bệnh nhân khỏi hệ thống: {ma} - {ten}")
                messagebox.showinfo(
                    "Thành công", f"Đã xóa bệnh nhân {ma} thành công!", parent=self
                )
                self.load_data_from_json()

    def search_data(self):
        """Tìm kiếm dữ liệu bệnh nhân"""
        query = self.ent_search.get().strip().lower()
        criterion = self.cbo_criterion.get()

        self.tree.delete(*self.tree.get_children())
        for item in self.data_list:
            match = False
            if criterion == "Mã BN / Tên":
                if (
                    query in item["MaBN"].lower()
                    or query in item["HoTen"].lower()
                ):
                    match = True
            elif criterion == "Số điện thoại":
                if query in item["SoDienThoai"].lower():
                    match = True

            if match or not query:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        item["MaBN"],
                        item["HoTen"],
                        item["SoDienThoai"],
                        item["GioiTinh"],
                        item["DiaChi"],
                    ),
                )

    def on_select_record(self, event):
        """Hiển thị dữ liệu lên form khi chọn dòng trên bảng"""
        selected = self.tree.selection()
        if selected:
            vals = self.tree.item(selected[0], "values")
            self.ent_mabn.config(state="normal")
            self.ent_mabn.delete(0, tk.END)
            self.ent_mabn.insert(0, vals[0])
            self.ent_mabn.config(state="readonly")

            self.ent_hoten.delete(0, tk.END)
            self.ent_hoten.insert(0, vals[1])

            self.ent_sdt.delete(0, tk.END)
            self.ent_sdt.insert(0, vals[2])

            self.cbo_gioitinh.set(vals[3])

            self.ent_diachi.delete(0, tk.END)
            self.ent_diachi.insert(0, vals[4])

    def clear_form(self):
        """Xóa trắng form nhập liệu"""
        self.ent_mabn.config(state="normal")
        self.ent_mabn.delete(0, tk.END)
        self.ent_hoten.delete(0, tk.END)
        self.ent_sdt.delete(0, tk.END)
        self.ent_diachi.delete(0, tk.END)
        self.cbo_gioitinh.set("Nam")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())