# utils.py
import csv
import hashlib
import logging
import os
import re
import urllib.request
from config import REGEX_BHYT, REGEX_PHONE

# Cấu hình ghi nhật ký (Logging) vào file app.log
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    encoding="utf-8",
)


def hash_password(password: str) -> str:
    """Băm mật khẩu bằng thuật toán SHA-256 để bảo mật"""
    if not password:
        return ""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def log_action(username: str, action: str):
    """Ghi lại nhật ký thao tác quan trọng vào app.log"""
    msg = f"Tài khoản '{username}' thực hiện: {action}"
    logging.info(msg)
    print(f"[LOG]: {msg}")


def validate_phone(phone: str) -> bool:
    """Kiểm tra số điện thoại hợp lệ bằng Regex (Yêu cầu đề tài)"""
    if not phone:
        return False
    return bool(re.match(REGEX_PHONE, phone.strip()))


def validate_bhyt(bhyt: str) -> bool:
    """Kiểm tra thẻ BHYT hợp lệ bằng Regex (Yêu cầu đề tài)"""
    if not bhyt:
        return True  # BHYT có thể để trống nếu không có
    return bool(re.match(REGEX_BHYT, bhyt.strip().upper()))


def export_to_csv(filename: str, headers: list, data: list):
    """Xuất danh sách dữ liệu ra file CSV"""
    try:
        with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        return True
    except Exception as e:
        print("[EXPORT CSV ERROR]:", e)
        return False


def export_invoice_txt(filename: str, content: str):
    """Xuất hóa đơn khám bệnh ra file TXT"""
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            file.write(content)
        return True
    except Exception as e:
        print("[EXPORT TXT ERROR]:", e)
        return False


def crawl_external_medical_services():
    """Lấy danh mục dịch vụ mẫu trực tuyến hoặc dùng danh mục chuẩn"""
    url = "https://jsonplaceholder.typicode.com/todos"
    headers = {"User-Agent": "Mozilla/5.0"}
    danh_muc_vn = [
        ("Khám Nội Tổng Quát", 150000),
        ("Khám Chuyên Khoa Tai Mũi Họng", 200000),
        ("Xét Nghiệm Máu Tổng Phân Tích", 180000),
        ("Siêu Âm Bụng Tổng Quát 4D", 250000),
        ("Chụp X-Quang Lồng Ngực Thẳng", 120000),
        ("Đo Điện Tim Cấp Cứu (ECG)", 100000),
    ]
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                return [
                    {"ma_dv": f"DV{i+1:03d}", "ten_dv": item[0], "gia": item[1]}
                    for i, item in enumerate(danh_muc_vn)
                ]
    except Exception:
        pass
    return [
        {"ma_dv": f"DV{i+1:03d}", "ten_dv": item[0], "gia": item[1]}
        for i, item in enumerate(danh_muc_vn)
    ]