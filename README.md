# QuanLyPhongKham
Hệ thống quản lý phòng khám được viết bằng python (Tinker và GUI). Hỗ trợ quản lý bệnh nhân, bác sĩ, Đăng Kí Lịch Khám, Dịch Vụ, Phân ca làm việc và xuất báo cáo CSV.
# 🏥 QuanLyPhongKham

Hệ thống **quản lý phòng khám** viết bằng **Python (Tkinter)** với giao diện GUI. Ứng dụng hỗ trợ quản lý bệnh nhân, bác sĩ, đăng ký lịch khám, dịch vụ, phân ca làm việc và xuất báo cáo CSV.

## 📌 Tính năng chính

- **Quản lý bệnh nhân**: thêm, sửa, xóa, tìm kiếm thông tin bệnh nhân.
- **Quản lý bác sĩ**: lưu và cập nhật thông tin bác sĩ.
- **Đăng ký lịch khám**: đặt lịch hẹn cho bệnh nhân, tra cứu lịch theo ngày.
- **Quản lý dịch vụ**: danh mục dịch vụ khám, có thể lấy dữ liệu từ nguồn bên ngoài thông qua `services/api_crawler.py`.
- **Phân ca làm việc**: quản lý lịch làm việc của bác sĩ.
- **Dashboard thống kê**: tổng quan số lượt khám và doanh thu (`dashboard.py`).
- **Xuất báo cáo CSV**: xuất báo cáo lịch khám (`bao_cao_lich_kham.csv`) và danh sách lịch hẹn (`danh_sach_lich_hen.csv`).

## 🛠️ Công nghệ sử dụng

| Thành phần | Mô tả |
|---|---|
| Ngôn ngữ | Python 3.x |
| Giao diện | Tkinter (GUI) |
| Lưu trữ dữ liệu | File JSON trong thư mục `db/` |
| Báo cáo | File CSV |
| Ghi log | `app.log` |

## 📂 Cấu trúc thư mục

```
source code/
├── db/
│   ├── __init__.py
│   ├── models.py                    # Định nghĩa các model dữ liệu
│   ├── data_bacsi.json              # Dữ liệu bác sĩ
│   ├── data_dichvu_crawled.json     # Dữ liệu dịch vụ (thu thập từ nguồn ngoài)
│   ├── data_lichkham.json           # Dữ liệu lịch khám
│   ├── data_lichlam.json            # Dữ liệu lịch làm việc / phân ca
│   ├── data_phongkham.json          # Dữ liệu phòng khám
│   └── bao_cao_lich_kham.csv        # Báo cáo lịch khám xuất ra
├── services/
│   └── api_crawler.py               # Thu thập dữ liệu dịch vụ
├── ui/                              # Các màn hình giao diện Tkinter
├── config.py                        # Cấu hình chung của ứng dụng
├── dashboard.py                     # Màn hình thống kê
├── main.py                          # File chạy chính của ứng dụng
├── utils.py                         # Các hàm tiện ích
├── data_phongkham.json              # Dữ liệu phòng khám
├── danh_sach_lich_hen.csv           # Danh sách lịch hẹn xuất ra
├── app.log                          # Log của ứng dụng
├── SOURCE_NOTES.md                  # Ghi chú về mã nguồn
└── README.md
```

## ⚙️ Yêu cầu hệ thống

- Python **3.8** trở lên
- Tkinter (đi kèm sẵn khi cài Python trên Windows và macOS; trên Linux cài thêm `python3-tk`)

Nếu dự án dùng thêm thư viện ngoài (ví dụ `tkcalendar`, `requests`...), cài bằng:

```bash
pip install -r requirements.txt
```

## 🚀 Cài đặt và chạy

1. **Clone dự án**

   ```bash
   git clone https://github.com/donggo113/QuanLyPhongKham.git
   cd QuanLyPhongKham
   ```

2. **(Tùy chọn) Tạo môi trường ảo**

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```

3. **Chạy ứng dụng**

   ```bash
   python main.py
   ```

## 📖 Hướng dẫn sử dụng

1. Mở ứng dụng bằng `python main.py`.
2. Dùng thanh điều hướng để chuyển giữa các chức năng: bệnh nhân, bác sĩ, lịch khám, dịch vụ, phân ca.
3. Thêm hoặc chỉnh sửa dữ liệu qua các biểu mẫu; dữ liệu được lưu vào các file JSON trong thư mục `db/`.
4. Vào mục báo cáo để xuất danh sách lịch khám / lịch hẹn ra file CSV.
5. Xem số liệu tổng quan ở màn hình Dashboard.

## 📝 Ghi chú

- Dữ liệu lưu dạng JSON nên không cần cài đặt cơ sở dữ liệu riêng.
- Thông tin chi tiết về mã nguồn xem thêm trong [`SOURCE_NOTES.md`](SOURCE_NOTES.md).
- Log lỗi và hoạt động của ứng dụng được ghi vào `app.log`.

## 🔮 Hướng phát triển

- Chuyển lưu trữ sang cơ sở dữ liệu (SQLite / SQL Server).
- Thêm đăng nhập và phân quyền người dùng.
- In phiếu khám và đơn thuốc.
- Biểu đồ thống kê doanh thu theo thời gian.

## 👤 Tác giả

**donggo113** – [github.com/donggo113](https://github.com/donggo113)
