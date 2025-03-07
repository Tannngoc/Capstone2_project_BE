import yfinance as yf
import pandas as pd
import numpy as np
import os

# Danh sách mã cổ phiếu muốn lấy dữ liệu
tickers = ['NVDA', 'TSLA', 'KO', 'IBM']
max_rows = 2468

save_dir = "app/db"
os.makedirs(save_dir, exist_ok=True)

def add_indicators(data):
    """Thêm các chỉ báo kỹ thuật vào dữ liệu cổ phiếu"""
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI_14'] = 100 - (100 / (1 + rs))

    data['MACD'] = data['Close'].ewm(span=12, adjust=False).mean() - data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    data['Daily_Return'] = data['Close'].pct_change()
    data['Volatility'] = data['Daily_Return'].rolling(window=20).std()

    data['Day_of_Week'] = data.index.dayofweek
    data['Day_of_Month'] = data.index.day
    data['Month'] = data.index.month
    data['Year'] = data.index.year

    data.dropna(inplace=True)
    return data

def clean_csv(file_path):
    """Xử lý lỗi định dạng trong file CSV"""
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, index_col=0, parse_dates=True, low_memory=False)
        
        # Xóa các cột bị lặp
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Chuẩn hóa tên cột
        df.columns = [col.strip("(')").split(",")[0].strip() for col in df.columns]
        
        # Xóa hàng chứa quá nhiều giá trị trống
        df.dropna(thresh=len(df.columns) // 2, inplace=True)

        # Lưu lại file đã sửa
        df.to_csv(file_path, index=True, encoding='utf-8-sig', float_format="%.6f")

for ticker in tickers:
    file_path = os.path.join(save_dir, f"{ticker}_stock.csv")
    print(f"📥 Đang lưu file tại: {os.path.abspath(file_path)}")

    # Đọc dữ liệu cũ (nếu có)
    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path, index_col=0, parse_dates=True)
    else:
        df_old = pd.DataFrame()

    print(f"🔄 Đang lấy dữ liệu cho: {ticker}")

    # Lấy dữ liệu mới từ Yahoo Finance
    new_data = yf.download(ticker, period='10y', interval='1d')

    if new_data.empty:
        print(f"⚠️ Không có dữ liệu mới cho {ticker}")
        continue

    new_data = add_indicators(new_data)

    # Gộp dữ liệu cũ và mới
    df = pd.concat([df_old, new_data])

    # Giới hạn số dòng
    df = df.tail(max_rows)

    # Lưu dữ liệu vào file CSV
    df.to_csv(file_path, index=True, encoding='utf-8-sig')

    # Sửa lỗi định dạng file CSV
    clean_csv(file_path)

print("✅ Hoàn thành cập nhật dữ liệu!")
