import os
import pandas as pd
from app import create_app, db
from app.models import StockPrice, Stock
from datetime import datetime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Tắt warning TensorFlow nếu cần

app = create_app()

def get_stock_id(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first()
    return stock.id if stock else None

def create_tables():
    with app.app_context():
        db.create_all()
        print("✅ Đã tạo bảng (nếu chưa có).")

def import_csv(file_path, stock_symbol):
    df = pd.read_csv(file_path)
    df['Price'] = pd.to_datetime(df['Price'])

    with app.app_context():
        stock_id = get_stock_id(stock_symbol)
        if not stock_id:
            print(f"⚠ Lỗi: Không tìm thấy {stock_symbol} trong bảng stocks!")
            return

        # Query toàn bộ date đang có
        existing_dates = set(
            date for (date,) in db.session.query(StockPrice.date)
            .filter_by(stock_id=stock_id)
            .all()
        )

        new_rows = []
        update_count = 0
        insert_count = 0

        for _, row in df.iterrows():
            date = row['Price']
            if date in existing_dates:
                # Update existing records
                db.session.query(StockPrice).filter_by(stock_id=stock_id, date=date).update({
                    'open_price': row['Open'],
                    'high_price': row['High'],
                    'low_price': row['Low'],
                    'close_price': row['Close'],
                    'volume': row['Volume']
                })
                update_count += 1
            else:
                new_rows.append(StockPrice(
                    stock_id=stock_id,
                    date=date,
                    open_price=row['Open'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    close_price=row['Close'],
                    volume=row['Volume']
                ))
                insert_count += 1

        # Bulk insert tất cả record mới
        if new_rows:
            db.session.bulk_save_objects(new_rows)

        db.session.commit()
        print(f"✅ Imported {insert_count} new rows, updated {update_count} rows for {stock_symbol}")

if __name__ == "__main__":
    create_tables()

    folder_path = "app/db"
    stock_files = ["AAPL_stock.csv", "IBM_stock.csv", "MSFT_stock.csv", "NVDA_stock.csv", "TSLA_stock.csv"]

    with app.app_context():
        for file_name in stock_files:
            stock_symbol = file_name.split("_")[0]
            file_path = os.path.join(folder_path, file_name)

            if os.path.exists(file_path):
                import_csv(file_path, stock_symbol)
            else:
                print(f"⚠ File {file_name} không tồn tại!")

