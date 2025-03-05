import yfinance as yf
import pandas as pd
import numpy as np
import os

# Danh sách mã cổ phiếu muốn lấy dữ liệu
tickers = ['NVDA', 'TSLA', 'KO', 'IBM']
max_rows = 2468  # Giới hạn số dòng tối đa

# Hàm tính toán các chỉ báo kỹ thuật và trường dữ liệu bổ sung
def add_indicators(data):
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

# Lặp qua từng cổ phiếu để cập nhật dữ liệu
for ticker in tickers:
    file_path = f"{ticker}_stock.csv"

    # Kiểm tra nếu file đã tồn tại để đọc dữ liệu cũ
    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path, index_col=0, parse_dates=True)
    else:
        df_old = pd.DataFrame()

    print(f"Đang lấy dữ liệu cho: {ticker}")
    
    # Lấy dữ liệu mới nhất
    new_data = yf.download(ticker, period='10y', interval='1d')

    if new_data.empty:
        print(f"Không có dữ liệu mới cho {ticker}")
        continue

    new_data = add_indicators(new_data)

    df = pd.concat([df_old, new_data])

    df = df.tail(max_rows)

    df.to_csv(file_path, index=True, encoding='utf-8-sig')
    print(f"Đã cập nhật dữ liệu cho {ticker} ({len(df)} dòng)")
