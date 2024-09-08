# apps/stock_crawlers/fetch_yahoo_finance.py

import os
from flask import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import datetime
import csv

def get_time_s(timestr):
    dt = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
    timestamp = int(dt.timestamp())
    return timestamp

def fetch_yahoo_finance(market_code):
    url = f"https://finance.yahoo.com/quote/{market_code}/history/"
    url += "?period1=" + str(get_time_s('2000-08-19 00:00:00'))
    url += "&period2=" + str(get_time_s(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chromedriver_path = os.path.join(os.path.dirname(__file__), 'chromedriver', 'chromedriver.exe')
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table.yf-ewueuo'))
        )
        outer_html = element.get_attribute('outerHTML')
        soup = BeautifulSoup(outer_html, 'html.parser')
        table = soup.find('table')
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            row_data = [col.get_text(strip=True) for col in columns]
            # 過濾掉包含非數值資料的行
            if all(col.replace('.', '', 1).isdigit() for col in row_data[1:5]):
                rows.append(row_data)

        # 轉換資料格式
        formatted_data = []
        for row in rows:
            try:
                date = datetime.datetime.strptime(row[0], '%b %d, %Y').timestamp() * 1000
                open_price = float(row[1])
                high_price = float(row[2])
                low_price = float(row[3])
                close_price = float(row[4])
                formatted_data.append({
                    'Date': date,
                    'Open': open_price,
                    'High': high_price,
                    'Low': low_price,
                    'Close': close_price
                })
            except ValueError:
                continue

        # 準備存檔資料
        result = [['Date', 'Open', 'High', 'Low', 'Close']]
        for record in formatted_data:
            result.append([
                datetime.datetime.fromtimestamp(record['Date'] / 1000).strftime('%b %d, %Y'),
                record['Open'],
                record['High'],
                record['Low'],
                record['Close']
            ])

        download_dir = os.path.abspath(os.path.join('apps', 'data', 'historical_data'))
        try:
            # 刪除 market_code 中的 .TWO
            if ".TWO" in market_code:
                market_code = market_code.replace(".TWO", "")

            os.makedirs(download_dir, exist_ok=True)
            file_path = os.path.join(download_dir, f"{market_code}.csv")
            
            # 檢查文件是否存在，存在則刪除
            if os.path.exists(file_path):
                os.remove(file_path)
            
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerows(result)

        except PermissionError as e:
            logging.error(f"沒有權限: {e}")
        except Exception as e:
            logging.error(f"發生錯誤: {e}")

        return formatted_data

    except TimeoutException:
        print("TimeoutException: 加載表格超時")
        return None
    finally:
        driver.quit()
