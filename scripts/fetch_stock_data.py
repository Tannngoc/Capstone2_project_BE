import yfinance as yf
import pandas as pd
import os

# Danh sách mã cổ phiếu cần lấy dữ liệu
TICKERS = ['NVDA', 'TSLA', 'MSFT', 'IBM', 'AAPL']
MAX_ROWS = 2468

SAVE_DIR = "app/db"
os.makedirs(SAVE_DIR, exist_ok=True)


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

    # Chỉ xóa các hàng có toàn bộ giá trị NaN, tránh xóa quá nhiều dữ liệu
    data.dropna(how="all", inplace=True)
    return data


def clean_csv(file_path):
    """Xóa dòng thứ 2 và thứ 3 trong file CSV"""
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, index_col=0, parse_dates=True, low_memory=False)

        # Giữ nguyên dòng đầu (tên cột), xóa dòng thứ 2 và 3
        df = df.iloc[2:].reset_index()

        # Lưu lại file CSV đã làm sạch
        df.to_csv(file_path, index=False, encoding='utf-8-sig', float_format="%.6f")
        print(f"✅ Đã làm sạch dữ liệu: {file_path}")


def fetch_stock_data(ticker):
    file_path = os.path.join(SAVE_DIR, f"{ticker}_stock.csv")

    # Xóa file cũ nếu tồn tại
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️ Đã xóa file cũ: {file_path}")

    print(f"📥 Đang lưu file mới tại: {os.path.abspath(file_path)}")

    # Tải dữ liệu mới từ yfinance
    print(f"🔄 Đang lấy dữ liệu cho: {ticker}")
    new_data = yf.download(ticker, period='10y', interval='1d')

    if new_data.empty:
        print(f"⚠️ Không có dữ liệu mới cho {ticker}")
        return

    # Thêm chỉ báo kỹ thuật
    new_data = add_indicators(new_data)

    # Giới hạn số dòng tối đa
    new_data = new_data.tail(MAX_ROWS)

    # Xóa cột bị lặp (nếu có)
    new_data = new_data.loc[:, ~new_data.columns.duplicated()]

    # Lưu dữ liệu mới vào file
    new_data.to_csv(file_path, index=True, encoding='utf-8-sig')

    # Làm sạch file sau khi cập nhật
    clean_csv(file_path)
    print(f"✅ Đã tạo file dữ liệu mới cho {ticker}")


# Chạy script cho tất cả mã cổ phiếu
for ticker in TICKERS:
    fetch_stock_data(ticker)

print("🎯 Hoàn thành cập nhật dữ liệu!")
