# apps/fastapi/taiex_api/price_requests.py

import requests
import logging

def get_exchange_price_list():
    url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
    headers = {
        "accept": "application/json",
        "If-Modified-Since": "Mon, 26 Jul 1997 05:00:00 GMT",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 確保請求成功
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching news data: {e}")
        return None

