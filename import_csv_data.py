import os
import pandas as pd
from app import create_app, db
from app.models import StockPrice, Stock
from datetime import datetime

app = create_app()

def get_stock_id(symbol):
    """Lấy stock_id từ bảng stocks dựa trên symbol"""
    stock = Stock.query.filter_by(symbol=symbol).first()
    return stock.id if stock else None

def import_csv(file_path, stock_symbol):
    """Import dữ liệu từ CSV vào bảng stock_prices với upsert"""
    df = pd.read_csv(file_path)

    with app.app_context():
        stock_id = get_stock_id(stock_symbol)
        if not stock_id:
            print(f"⚠ Lỗi: Không tìm thấy {stock_symbol} trong bảng stocks!")
            return

        imported_count = 0
        updated_count = 0

        for _, row in df.iterrows():
            date = datetime.strptime(row['Price'], "%Y-%m-%d")

            # Kiểm tra xem đã có dòng nào cho stock_id + date chưa
            existing = StockPrice.query.filter_by(stock_id=stock_id, date=date).first()

            if existing:
                # Cập nhật nếu đã có
                existing.open_price = row['Open']
                existing.high_price = row['High']
                existing.low_price = row['Low']
                existing.close_price = row['Close']
                existing.volume = row['Volume']
                updated_count += 1
            else:
                # Thêm mới nếu chưa có
                new_price = StockPrice(
                    stock_id=stock_id,
                    date=date,
                    open_price=row['Open'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    close_price=row['Close'],
                    volume=row['Volume']
                )
                db.session.add(new_price)
                imported_count += 1

        db.session.commit()
        print(f"✅ Imported {imported_count} new rows, updated {updated_count} rows for {stock_symbol}")

if __name__ == "__main__":
    folder_path = "app/db"  # Thư mục chứa CSV
    stock_files = ["AAPL_stock.csv", "IBM_stock.csv", "MSFT_stock.csv", "NVDA_stock.csv", "TSLA_stock.csv"]

    with app.app_context():
        for file_name in stock_files:
            stock_symbol = file_name.split("_")[0]  # Tự động lấy mã chứng khoán từ tên file
            file_path = os.path.join(folder_path, file_name)

            if os.path.exists(file_path):
                import_csv(file_path, stock_symbol)
            else:
                print(f"⚠ File {file_name} không tồn tại!")

