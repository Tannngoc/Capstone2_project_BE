from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import dateparser
from datetime import datetime, timedelta
import os

# Cài đặt trình duyệt headless
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

tickers = ['AAPL', 'IBM', 'TSLA', 'MSFT', 'NVDA']
base_url = "https://finance.yahoo.com/quote/{}/news"
news_data = []

# Tính ngày và giờ của 24 giờ qua
cutoff_time = datetime.now() - timedelta(days=1)

# Đảm bảo thư mục tồn tại
output_path = "app/db/news.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Kiểm tra xem file đã tồn tại chưa và nếu có thì load dữ liệu hiện tại
if os.path.exists(output_path):
    existing_df = pd.read_csv(output_path)
    existing_titles = set(existing_df['title'] + existing_df['published_date'].astype(str))  # Kết hợp title và published_date
else:
    existing_titles = set()

for ticker in tickers:
    print(f"\n📥 Fetching news for {ticker}...")
    url = base_url.format(ticker)
    driver.get(url)

    # Lấy toàn bộ các bài viết trên trang mà không cần cuộn trang
    articles = driver.find_elements(By.CSS_SELECTOR, 'section[role="article"]')

    for article in articles:
        try:
            title_elem = article.find_element(By.TAG_NAME, 'h3')
            title = title_elem.text.strip()

            # Lấy thông tin thời gian
            pub_info = article.find_element(By.CSS_SELECTOR, 'div.publishing').text.strip()
            if '•' in pub_info:
                _, published_time = map(str.strip, pub_info.split('•', 1))
            else:
                published_time = pub_info.strip()

            # Phân tích thời gian đăng bài
            pub_date = dateparser.parse(published_time)
            if pub_date is None or pub_date < cutoff_time:
                continue  # Chỉ lấy tin trong 24 giờ qua

            # Tạo khóa duy nhất để kiểm tra trùng lặp: sử dụng title và published_date
            unique_key = title + pub_date.strftime('%Y-%m-%d')

            # Kiểm tra trùng lặp dựa trên khóa duy nhất
            if unique_key in existing_titles:
                continue  # Bỏ qua bài viết đã có

            # Lưu tin vào danh sách
            news_data.append({
                'company': ticker,
                'title': title,
                'published_date': pub_date.strftime('%Y-%m-%d')
            })

            # Thêm vào set để tránh lưu trùng trong quá trình này
            existing_titles.add(unique_key)

        except Exception as e:
            continue  # Bỏ qua bài viết có lỗi

driver.quit()

# Nếu có dữ liệu mới, append vào file
if news_data:
    new_df = pd.DataFrame(news_data)
    new_df.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False, encoding='utf-8-sig')
    print(f"\n✅ Đã lưu {len(new_df)} bài viết vào '{output_path}'")
else:
    print("\n⚠️ Không có tin tức mới để lưu.")