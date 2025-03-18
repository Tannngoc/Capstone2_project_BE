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
    """Import dữ liệu từ CSV vào bảng stock_prices"""
    df = pd.read_csv(file_path)

    with app.app_context():
        stock_id = get_stock_id(stock_symbol)
        if not stock_id:
            print(f"⚠ Lỗi: Không tìm thấy {stock_symbol} trong bảng stocks!")
            return

        stock_prices = [
            StockPrice(
                stock_id=stock_id,
                date=datetime.strptime(row['Price'], "%Y-%m-%d"),
                open_price=row['Open'],
                high_price=row['High'],
                low_price=row['Low'],
                close_price=row['Close'],
                volume=row['Volume']
            )
            for _, row in df.iterrows()
        ]

        db.session.bulk_save_objects(stock_prices)  # Thêm nhanh nhiều dòng
        db.session.commit()
        print(f"✅ Imported {len(df)} rows for {stock_symbol}")

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

