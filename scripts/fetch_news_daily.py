from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import dateparser
from datetime import datetime, timedelta
import os
import sys

# Cài đặt trình duyệt headless
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-tools')

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"❌ Failed to initialize headless Chrome: {e}")
    sys.exit(1)

tickers = ['AAPL', 'IBM', 'TSLA', 'MSFT', 'NVDA']
base_url = "https://finance.yahoo.com/quote/{}/news"
news_data = []

# Tính thời gian cắt mốc 24 giờ
cutoff_time = datetime.now() - timedelta(days=1)

# Tạo thư mục chứa file nếu chưa tồn tại
output_path = "app/db/news.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Load dữ liệu cũ nếu có
if os.path.exists(output_path):
    existing_df = pd.read_csv(output_path)
    existing_titles = set(existing_df['title'] + existing_df['published_date'].astype(str))
else:
    existing_titles = set()

for ticker in tickers:
    print(f"\n📥 Fetching news for {ticker}...")
    url = base_url.format(ticker)
    try:
        driver.get(url)
    except Exception as e:
        print(f"❌ Failed to load page for {ticker}: {e}")
        continue

    try:
        articles = driver.find_elements(By.CSS_SELECTOR, 'section[role="article"]')
    except Exception as e:
        print(f"❌ Error finding articles for {ticker}: {e}")
        continue

    for article in articles:
        try:
            title_elem = article.find_element(By.TAG_NAME, 'h3')
            title = title_elem.text.strip()

            pub_info = article.find_element(By.CSS_SELECTOR, 'div.publishing').text.strip()
            if '•' in pub_info:
                _, published_time = map(str.strip, pub_info.split('•', 1))
            else:
                published_time = pub_info.strip()

            pub_date = dateparser.parse(published_time)
            if pub_date is None or pub_date < cutoff_time:
                continue

            unique_key = title + pub_date.strftime('%Y-%m-%d')
            if unique_key in existing_titles:
                continue

            news_data.append({
                'company': ticker,
                'title': title,
                'published_date': pub_date.strftime('%Y-%m-%d')
            })

            existing_titles.add(unique_key)

        except Exception as e:
            print(f"❌ Error parsing article for {ticker}: {e}")
            continue

driver.quit()

if news_data:
    new_df = pd.DataFrame(news_data)
    new_df.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False, encoding='utf-8-sig')
    print(f"\n✅ Đã lưu {len(new_df)} bài viết vào '{output_path}'")
else:
    print("\n⚠️ Không có tin tức mới để lưu.")
