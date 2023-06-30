# Sử dụng base image từ Docker Hub
FROM python:3.11

# Sao chép mã nguồn của chương trình vào trong container
COPY . /app

# Đặt thư mục làm việc mặc định trong container
WORKDIR /app

# Cài đặt các dependencies của chương trình
RUN pip install -r requirements.txt

# Chạy lệnh để thực hiện crawl dữ liệu (thay "crawl.py" bằng tên file chương trình thực tế của bạn)
CMD ["python", "crawl.py"]