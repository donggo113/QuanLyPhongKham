# ui/quanlybacsi.py
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from utils import log_action, validate_phone


class DoctorManagementView(tk.Frame):

    def __init__(self, parent, role="admin"):
        super().__init__(parent, bg="#FFFFFF")
        self.role = role
        self.db_file = os.path.join("db", "data_bacsi.json")
        self.data_list = []

        self.setup_ui()
        self.load_data_from_json()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#FFFFFF")
        header.pack(fill="x", pady=(0, 10))

        tk.Label(
            header,
            text="👨‍⚕️ QUẢN LÝ DANH SÁCH BÁC SĨ",
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")

        # 1. Khung Tìm Kiếm
        search_frame = tk.LabelFrame(
            self,
            text=" Tìm kiếm bác sĩ ",
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
        btn_search.grid(row=0, column=2, padx=5, pady=5)

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
        btn_refresh.grid(row=0, column=3, padx=5, pady=5)

        # 2. Bảng Treeview Bác sĩ
        table_frame = tk.Frame(self, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("MaBS", "HoTen", "ChuyenKhoa", "SoDienThoai", "Email")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=8
        )

        self.tree.heading("MaBS", text="Mã BS")
        self.tree.heading("HoTen", text="Họ và Tên")
        self.tree.heading("ChuyenKhoa", text="Chuyên Khoa")
        self.tree.heading("SoDienThoai", text="Số Điện Thoại")
        self.tree.heading("Email", text="Email")

        self.tree.column("MaBS", anchor="center", width=80)
        self.tree.column("HoTen", anchor="w", width=180)
        self.tree.column("ChuyenKhoa", anchor="w", width=140)
        self.tree.column("SoDienThoai", anchor="center", width=120)
        self.tree.column("Email", anchor="w", width=200)

        self.tree.pack(fill="both", expand=True, side="left")
        self.tree.bind("<<TreeviewSelect>>", self.on_select_record)

        # 3. Form nhập liệu Bác sĩ
        form_frame = tk.LabelFrame(
            self,
            text=" Thông tin bác sĩ ",
            bg="#FFFFFF",
            fg="#1C1917",
            font=("Segoe UI", 9, "bold"),
            bd=1,
            relief="solid",
        )
        form_frame.pack(fill="x", ipadx=10, ipady=5)

        tk.Label(
            form_frame, text="Mã Bác Sĩ:*", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.ent_mabs = ttk.Entry(form_frame, width=20)
        self.ent_mabs.grid(row=0, column=1, sticky="w", padx=5, pady=3)

        tk.Label(
            form_frame, text="Họ và Tên:*", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.ent_hoten = ttk.Entry(form_frame, width=35)
        self.ent_hoten.grid(row=0, column=3, sticky="w", padx=5, pady=3)

        tk.Label(
            form_frame, text="Chuyên Khoa:*", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.ent_ck = ttk.Entry(form_frame, width=20)
        self.ent_ck.grid(row=1, column=1, sticky="w", padx=5, pady=3)

        tk.Label(
            form_frame,
            text="Số Điện Thoại:*",
            bg="#FFFFFF",
            font=("Segoe UI", 9),
        ).grid(row=1, column=2, sticky="w", padx=5, pady=3)
        self.ent_sdt = ttk.Entry(form_frame, width=35)
        self.ent_sdt.grid(row=1, column=3, sticky="w", padx=5, pady=3)

        tk.Label(
            form_frame, text="Email:", bg="#FFFFFF", font=("Segoe UI", 9)
        ).grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.ent_email = ttk.Entry(form_frame, width=60)
        self.ent_email.grid(
            row=2, column=1, columnspan=3, sticky="w", padx=5, pady=3
        )

        # Thanh nút thao tác
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
        """Đọc file JSON, tự tạo dữ liệu mẫu 6 Bác sĩ nếu chưa có file"""
        self.tree.delete(*self.tree.get_children())
        self.data_list.clear()

        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    self.data_list = json.load(f)
            except Exception as e:
                self.data_list = []

        # TỰ ĐỘNG KHỞI TẠO 6 BÁC SĨ MẪU NẾU FILE CHƯA TỒN TẠI HẶC RỖNG
        if not self.data_list:
            self.data_list = [
                {
                    "MaBS": "BS001",
                    "HoTen": "PGS.TS Nguyễn Văn Bình",
                    "ChuyenKhoa": "Nội Tổng Quát",
                    "SoDienThoai": "0901234567",
                    "Email": "binh.nguyen@phongkham.vn",
                },
                {
                    "MaBS": "BS002",
                    "HoTen": "ThS.BS Trần Thị Mai",
                    "ChuyenKhoa": "Tai Mũi Họng",
                    "SoDienThoai": "0902345678",
                    "Email": "mai.tran@phongkham.vn",
                },
                {
                    "MaBS": "BS003",
                    "HoTen": "BS.CKII Lê Hoàng Nam",
                    "ChuyenKhoa": "Chẩn Đoán Hình Ảnh",
                    "SoDienThoai": "0903456789",
                    "Email": "nam.le@phongkham.vn",
                },
                {
                    "MaBS": "BS004",
                    "HoTen": "BS.CKI Phạm Thanh Hà",
                    "ChuyenKhoa": "Nhi Khoa",
                    "SoDienThoai": "0904567890",
                    "Email": "ha.pham@phongkham.vn",
                },
                {
                    "MaBS": "BS005",
                    "HoTen": "ThS.BS Đỗ Văn Khoa",
                    "ChuyenKhoa": "Tim Mạch",
                    "SoDienThoai": "0905678901",
                    "Email": "khoa.do@phongkham.vn",
                },
                {
                    "MaBS": "BS006",
                    "HoTen": "BS.CKI Nguyễn Thị Lan",
                    "ChuyenKhoa": "Da Liễu",
                    "SoDienThoai": "0906789012",
                    "Email": "lan.nguyen@phongkham.vn",
                },
            ]
            self.save_data_to_json()

        for item in self.data_list:
            self.tree.insert(
                "",
                "end",
                values=(
                    item["MaBS"],
                    item["HoTen"],
                    item["ChuyenKhoa"],
                    item["SoDienThoai"],
                    item.get("Email", ""),
                ),
            )
        self.clear_form()

    def save_data_to_json(self):
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
        ma = self.ent_mabs.get().strip().upper()
        ten = self.ent_hoten.get().strip()
        ck = self.ent_ck.get().strip()
        sdt = self.ent_sdt.get().strip()
        email = self.ent_email.get().strip()

        if not ma or not ten or not sdt or not ck:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng nhập đầy đủ các trường bắt buộc (*)",
                parent=self,
            )
            return

        if any(item["MaBS"] == ma for item in self.data_list):
            messagebox.showerror(
                "Lỗi trùng mã", f"Mã bác sĩ '{ma}' đã tồn tại!", parent=self
            )
            return

        if not validate_phone(sdt):
            messagebox.showerror(
                "Lỗi định dạng", "Số điện thoại không hợp lệ!", parent=self
            )
            return

        new_item = {
            "MaBS": ma,
            "HoTen": ten,
            "ChuyenKhoa": ck,
            "SoDienThoai": sdt,
            "Email": email,
        }
        self.data_list.append(new_item)

        if self.save_data_to_json():
            log_action(self.role, f"Thêm bác sĩ thành công: {ma} - {ten}")
            messagebox.showinfo(
                "Thành công", f"Đã thêm bác sĩ {ma} thành công!", parent=self
            )
            self.load_data_from_json()

    def update_record(self):
        ma = self.ent_mabs.get().strip().upper()
        ten = self.ent_hoten.get().strip()
        ck = self.ent_ck.get().strip()
        sdt = self.ent_sdt.get().strip()
        email = self.ent_email.get().strip()

        if not ma:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng chọn một bác sĩ từ bảng để chỉnh sửa!",
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
            if item["MaBS"] == ma:
                item["HoTen"] = ten
                item["ChuyenKhoa"] = ck
                item["SoDienThoai"] = sdt
                item["Email"] = email
                found = True
                break

        if found and self.save_data_to_json():
            log_action(self.role, f"Cập nhật thông tin bác sĩ: {ma}")
            messagebox.showinfo(
                "Thành công",
                f"Đã cập nhật dữ liệu bác sĩ {ma}!",
                parent=self,
            )
            self.load_data_from_json()

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Cảnh báo", "Vui lòng chọn bác sĩ cần xóa!", parent=self
            )
            return

        vals = self.tree.item(selected[0], "values")
        ma = vals[0]
        ten = vals[1]

        if messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa bác sĩ '{ten}' ({ma}) không?",
            parent=self,
        ):
            self.data_list = [
                item for item in self.data_list if item["MaBS"] != ma
            ]
            if self.save_data_to_json():
                log_action(self.role, f"Xóa bác sĩ khỏi hệ thống: {ma} - {ten}")
                messagebox.showinfo(
                    "Thành công", f"Đã xóa bác sĩ {ma} thành công!", parent=self
                )
                self.load_data_from_json()

    def search_data(self):
        query = self.ent_search.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        for item in self.data_list:
            if (
                query in item["MaBS"].lower()
                or query in item["HoTen"].lower()
                or query in item["ChuyenKhoa"].lower()
                or not query
            ):
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        item["MaBS"],
                        item["HoTen"],
                        item["ChuyenKhoa"],
                        item["SoDienThoai"],
                        item.get("Email", ""),
                    ),
                )

    def on_select_record(self, event):
        selected = self.tree.selection()
        if selected:
            vals = self.tree.item(selected[0], "values")
            self.ent_mabs.config(state="normal")
            self.ent_mabs.delete(0, tk.END)
            self.ent_mabs.insert(0, vals[0])
            self.ent_mabs.config(state="readonly")

            self.ent_hoten.delete(0, tk.END)
            self.ent_hoten.insert(0, vals[1])

            self.ent_ck.delete(0, tk.END)
            self.ent_ck.insert(0, vals[2])

            self.ent_sdt.delete(0, tk.END)
            self.ent_sdt.insert(0, vals[3])

            self.ent_email.delete(0, tk.END)
            self.ent_email.insert(0, vals[4])

    def clear_form(self):
        self.ent_mabs.config(state="normal")
        self.ent_mabs.delete(0, tk.END)
        self.ent_hoten.delete(0, tk.END)
        self.ent_ck.delete(0, tk.END)
        self.ent_sdt.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())