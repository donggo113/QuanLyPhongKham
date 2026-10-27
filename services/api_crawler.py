import json
import os
import requests


class DataCrawler:

    def __init__(
        self, db_path=os.path.join("db", "data_dichvu_crawled.json")
    ):
        self.db_path = db_path

    def crawl_or_fetch_api_data(self):
        """Lấy danh sách dịch vụ y tế mẫu từ API công khai, làm sạch và lưu vào file JSON."""
        # API công khai giả lập / endpoint chứa danh sách danh mục y tế
        url = "https://jsonplaceholder.typicode.com/posts"

        try:
            # Thiết lập timeout để xử lý trường hợp không phản hồi
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                raw_data = response.json()

                # Làm sạch và chuyển đổi dữ liệu thành danh mục dịch vụ phòng khám
                cleaned_data = []
                for idx, item in enumerate(raw_data[:10]):
                    cleaned_data.append({
                        "ma_dv": f"DV_API_{idx+1:02d}",
                        "ten_dich_vu": f"Dịch vụ Y tế {item['title'][:20].title()}",
                        "don_gia": (idx + 1) * 50000 + 100000,
                        "nguon": "API External Database",
                    })

                # Đảm bảo thư mục db tồn tại
                os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

                # Lưu vào file JSON
                with open(self.db_path, "w", encoding="utf-8") as f:
                    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

                return True, f"Đã đồng bộ {len(cleaned_data)} dịch vụ từ API!"
            else:
                return (
                    False,
                    f"Máy chủ phản hồi mã lỗi: {response.status_code}",
                )

        except requests.exceptions.Timeout:
            return (
                False,
                "Lỗi: Kết nối API vượt quá thời gian chờ (Timeout).",
            )
        except requests.exceptions.RequestException as e:
            return False, f"Lỗi kết nối mạng hoặc không thể gọi API: {str(e)}"
        except Exception as e:
            return False, f"Lỗi xử lý dữ liệu: {str(e)}"