from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import dateparser
from datetime import datetime, timedelta
import os

# Cài đặt trình duyệt headless
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

tickers = ['AAPL', 'IBM', 'TSLA', 'MSFT', 'NVDA']
base_url = "https://finance.yahoo.com/quote/{}/news"
news_data = []

cutoff_date = datetime.now() - timedelta(days=60)

for ticker in tickers:
    print(f"\n📥 Fetching news for {ticker}...")
    url = base_url.format(ticker)
    driver.get(url)
    time.sleep(3)

    seen = set()
    old_len = 0

    while True:
        articles = driver.find_elements(By.CSS_SELECTOR, 'section[role="article"]')

        for article in articles[old_len:]:
            try:
                title_elem = article.find_element(By.TAG_NAME, 'h3')
                title = title_elem.text.strip()
                if title in seen:
                    continue
                seen.add(title)

                pub_info = article.find_element(By.CSS_SELECTOR, 'div.publishing').text.strip()
                if '•' in pub_info:
                    _, published_time = map(str.strip, pub_info.split('•', 1))
                else:
                    published_time = pub_info.strip()

                pub_date = dateparser.parse(published_time)
                if pub_date is None or pub_date < cutoff_date:
                    continue

                news_data.append({
                    'company': ticker,
                    'title': title,
                    'published_date': pub_date.strftime('%Y-%m-%d')
                })
            except:
                continue

        old_len = len(articles)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_len = len(driver.find_elements(By.CSS_SELECTOR, 'section[role="article"]'))
        if new_len == old_len:
            print(f"✅ Dừng tại {len(seen)} bài (đã đủ hoặc hết bài trong 60 ngày).")
            break

driver.quit()

# Đảm bảo thư mục tồn tại
output_path = "app/db/news.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Lưu dữ liệu vào CSV
df = pd.DataFrame(news_data)
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ Đã lưu {len(df)} bài viết vào '{output_path}'")
