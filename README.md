# Capstone2_project_BE
# 1. Tạo môi trường ảo:
# - Trên MacOS và Linux:
#    python3 -m venv venv
#    source venv/bin/activate
# - Trên Windows:
#    python -m venv venv
#    .\venv\Scripts\activate

# 2. Cài các thư viện:
# pip install -r requirements.txt

# 4. Khởi tạo db:
# Chạy file starfall.sql trong mysql

# 3. Cấu hình cái đặt sql trong .env:
# DATABASE_URI=mysql+pymysql://taikhoan:matkhau@localhost:3306/tendb

# 4. Khởi tạo và cập nhật db:
# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade


B5: Đưa dữ liệu fetch api từ file csv vào db:
	bấm nút run chạy file import_csv_data.py

B6: Sau khi thêm dữ liệu vào hoàn tất,
	chạy dự án: flask run

B7: Test api: http://127.0.0.1:5000/api/stock-price/AAPL/2024/3 (Có thể thay tên doanh nghiệp và thời gian)

# 8. Cai dat github action ve may
# brew install act (mac)

# 6. Cai dat docker
# link:
# open docker: open -a Docker
# run: act -j fetch-data --bind

# Final: Chạy ứng dụng Flask:
# flask run



