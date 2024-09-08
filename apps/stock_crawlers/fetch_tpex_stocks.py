# apps.stock_crawlers.fetch_tpex_stocks.py

# 撈櫃買中心上櫃.興櫃的股票代碼
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def create_driver():
    chromedriver_path = os.path.join(os.path.dirname(__file__), 'chromedriver', 'chromedriver.exe')
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)
    return driver

def fetch_otc_stocks(driver):
    # 打開目標網頁 上櫃
    driver.get("https://www.tpex.org.tw/web/regular_emerging/corporateInfo/regular/regular_stock.php?l=zh-tw")

    # 選擇本國企業股票
    select = Select(driver.find_element(By.ID, 'stk_type'))
    select.select_by_visible_text('本國企業股票')

    # 點擊查詢按鈕
    query_button = driver.find_element(By.NAME, 'btnQuery')
    query_button.click()

    # 等待頁面加載
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'company_list')))

    # 選擇顯示 100 筆資料
    company_list_length = Select(driver.find_element(By.NAME, 'company_list_length'))
    company_list_length.select_by_value('100')

    # 等待頁面加載
    time.sleep(2)

    # 提取所有分頁中的數據
    stocks = []
    while True:
        # 解析 HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 找到股票代碼的表格
        table = soup.find('table', {'id': 'company_list'})

        # 提取表格中的數據
        for row in table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            stock_code = cols[0].text.strip()
            company_name = cols[1].text.strip()
            net_value = cols[2].text.strip()
            industry = cols[3].text.strip()
            stocks.append({
                '股票代號': stock_code,
                '公司名稱': company_name,
                '最新一季每股淨值(元)': net_value,
                '產業類別': industry
            })

        # 檢查是否有下一頁按鈕
        next_button = driver.find_element(By.ID, 'company_list_next')
        if 'disabled' in next_button.get_attribute('class'):
            break
        else:
            next_button.click()
            time.sleep(2)  # 等待頁面加載

    return stocks

def fetch_esm_stocks(driver):
    # 打開目標網頁 興櫃
    driver.get("https://www.tpex.org.tw/web/regular_emerging/corporateInfo/emerging/emerging_stock.php?l=zh-tw")

    # 選擇本國企業股票
    select = Select(driver.find_element(By.ID, 'stk_type'))
    select.select_by_visible_text('本國企業股票')

    # 點擊查詢按鈕
    query_button = driver.find_element(By.NAME, 'btnQuery')
    query_button.click()

    # 等待頁面加載
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'company_list')))

    # 選擇顯示 100 筆資料
    company_list_length = Select(driver.find_element(By.NAME, 'company_list_length'))
    company_list_length.select_by_value('100')

    # 等待頁面加載
    time.sleep(2)

    # 提取所有分頁中的數據
    stocks = []
    while True:
        # 解析 HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 找到股票代碼的表格
        table = soup.find('table', {'id': 'company_list'})

        # 提取表格中的數據
        for row in table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            stock_code = cols[0].text.strip()
            company_name = cols[1].text.strip()
            net_value = cols[2].text.strip()
            industry = cols[3].text.strip()
            stocks.append({
                '股票代號': stock_code,
                '公司名稱': company_name,
                '最新一季每股淨值(元)': net_value,
                '產業類別': industry
            })

        # 檢查是否有下一頁按鈕
        next_button = driver.find_element(By.ID, 'company_list_next')
        if 'disabled' in next_button.get_attribute('class'):
            break
        else:
            next_button.click()
            time.sleep(2)  # 等待頁面加載

    return stocks

def save_to_csv(stocks, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['股票代號', '公司名稱', '最新一季每股淨值(元)', '產業類別']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for stock in stocks:
            writer.writerow(stock)

# 執行爬取任務
driver = create_driver()
otc_stocks = fetch_otc_stocks(driver)
esm_stocks = fetch_esm_stocks(driver)
driver.quit()

# 儲存股票數據到 CSV 文件
os.makedirs('data', exist_ok=True)
save_to_csv(otc_stocks, 'data/otc_stocks.csv')
save_to_csv(esm_stocks, 'data/esm_stocks.csv')


# 輸出股票數據
print("上櫃股票:")
for stock in otc_stocks:
    print(stock)

print("\n興櫃股票:")
for stock in esm_stocks:
    print(stock)
