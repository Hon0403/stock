import requests
import pandas as pd
from io import StringIO

def fetch_stock_data(stock_id, date):
    url = 'https://www.tpex.org.tw/web/emergingstock/single_historical/history.php?l=zh-tw'
    params = {
        'stk_code': stock_id,
        'date': date
    }
    response = requests.get(url, params=params)
    print("HTTP Status Code:", response.status_code)
    print("Response Content:", response.text)  # 打印回傳的內容
    if response.ok:
        try:
            data = response.json()
            if 'aaData' in data:
                df = pd.DataFrame(data['aaData'])
                return df
            else:
                return None
        except ValueError as e:
            print("JSON Decode Error:", e)
            return None
    else:
        return None

# 測試函數
stock_id = '1260'  # 替換為實際的股票代號
date = '112/02'  # 替換為實際的日期
stock_data = fetch_stock_data(stock_id, date)
if stock_data is not None:
    print(stock_data)
else:
    print("無法取得資料")
