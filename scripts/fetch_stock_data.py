import yfinance as yf
import pandas as pd
import numpy as np
import os

# Danh sách mã cổ phiếu cần lấy dữ liệu
tickers = ['NVDA', 'TSLA', 'KO', 'IBM']
max_rows = 2468  # Giữ lại số lượng dòng tối đa

save_dir = "app/db"
os.makedirs(save_dir, exist_ok=True)  # Tạo thư mục nếu chưa có

def add_indicators(data):
    """Thêm các chỉ báo kỹ thuật vào dữ liệu."""
    data = data.copy()  # Đảm bảo không thay đổi dữ liệu gốc
    
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

    # Chỉ xóa dòng có quá nhiều giá trị NaN
    data.dropna(subset=['SMA_20', 'SMA_50', 'RSI_14', 'MACD', 'MACD_Signal'], inplace=True)

    return data

for ticker in tickers:
    file_path = os.path.join(save_dir, f"{ticker}_stock.csv")
    print(f"📂 Lưu dữ liệu tại: {os.path.abspath(file_path)}")

    # Đọc dữ liệu cũ nếu tồn tại
    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path, index_col=0, parse_dates=True)
    else:
        df_old = pd.DataFrame()

    print(f"📈 Đang lấy dữ liệu cho: {ticker}")

    # Lấy dữ liệu mới nhất
    new_data = yf.download(ticker, period='10y', interval='1d')

    if new_data.empty:
        print(f"⚠️ Không có dữ liệu mới cho {ticker}")
        continue

    print(f"✅ Dữ liệu tải về ({ticker}): {new_data.shape[0]} dòng")

    # Thêm các chỉ báo kỹ thuật
    new_data = add_indicators(new_data)

    # Xóa dữ liệu trùng lặp, chỉ giữ lại dữ liệu mới
    df_old = df_old[~df_old.index.isin(new_data.index)]
    df = pd.concat([df_old, new_data]).tail(max_rows)  # Giữ lại max_rows dòng

    # Chuẩn hóa tên cột để tránh lỗi format
    df.columns = [col.replace(" ", "_") for col in df.columns]

    # Lưu file CSV với định dạng chuẩn
    df.to_csv(file_path, index=True, encoding='utf-8-sig', float_format="%.6f")

    print(f"💾 Đã lưu dữ liệu cho {ticker}")

print("🎉 Hoàn thành cập nhật dữ liệu!")
