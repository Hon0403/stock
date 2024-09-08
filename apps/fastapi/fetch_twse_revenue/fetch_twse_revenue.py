import requests
import json

# API URL
url = "https://openapi.twse.com.tw/v1/opendata/t187ap05_P"

# 發送GET請求
response = requests.get(url, headers={
    "accept": "application/json",
    "If-Modified-Since": "Mon, 26 Jul 1997 05:00:00 GMT",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
})

# 檢查請求是否成功
if response.status_code == 200:
    # 解析JSON數據
    data = response.json()
    

else:
    print(f"請求失敗，狀態碼: {response.status_code}")