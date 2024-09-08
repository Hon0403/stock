# apps/fastapi/tpex_all_api/tpex_all_quotes/tpex_all_quotes.py

import requests
from typing import Optional, Dict, List

def fetch_tpex_mainboard_quotes(market_code: str) -> Optional[List[Dict]]:
    """
    從 TPEX 主板報價 API 獲取資料。

    Args:
        market_code (str): 公司的市場代碼。

    Returns:
        list: 從 API 獲取的資料列表。
    """
    url = f"https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes?market_code={market_code}"
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"網路錯誤: {e}")
    except ValueError as e:
        raise RuntimeError(f"JSON 解析錯誤: {e}")

def fetch_tpex_esm_latest_statistics(market_code: str) -> Optional[List[Dict]]:
    """
    從 TPEX ESM 最新統計 API 獲取資料。

    Args:
        market_code (str): 公司的市場代碼。

    Returns:
        list: 從 API 獲取的資料列表。
    """
    url = f"https://www.tpex.org.tw/openapi/v1/tpex_esb_latest_statistics?market_code={market_code}"
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"網路錯誤: {e}")
    except ValueError as e:
        raise RuntimeError(f"JSON 解析錯誤: {e}")

def process_market_data(data: List[Dict], market_code: str, market_type: str) -> Dict:
    """
    根據 market_type 處理市場數據並計算變動值和百分比。

    Args:
        data (list): API 返回的市場數據。
        market_code (str): 公司的市場代碼。
        market_type (str): 市場類型 ('otc' 或 'esm')。

    Returns:
        dict: 處理後的市場數據。
    """
    market_data = next((item for item in data if item.get("SecuritiesCompanyCode") == market_code), None)
    
    if market_data:
        if market_type == 'otc':
            market_data = {
                "name": market_data.get("CompanyName"),
                "code": market_data.get("SecuritiesCompanyCode"),
                "Open": market_data.get("Open"),
                "High": market_data.get("High"),
                "Low": market_data.get("Low"),
                "Close": market_data.get("Close"),
                "change": market_data.get("Change"),
                "changePercent": market_data.get("ChangePercent"),
                "TradingShares": market_data.get("TradingShares"),
                "TransactionAmount": market_data.get("TransactionAmount")
            }
        elif market_type == 'esm':
            market_data = {
                "name": market_data.get("CompanyName"),
                "code": market_data.get("SecuritiesCompanyCode"),
                "Open": market_data.get("PreviousAveragePrice"),
                "High": market_data.get("Highest"),
                "Low": market_data.get("Lowest"),
                "Close": market_data.get("LatestPrice"),
                "change": None,  # 這裡可以根據需要計算變動值
                "changePercent": None,  # 這裡可以根據需要計算變動百分比
                "TradingShares": market_data.get("TransactionVolume"),
                "TransactionAmount": None  # 這裡可以根據需要計算成交值
            }

        # 計算變動值和變動百分比
        current_price = market_data.get("Close") if market_type == 'otc' else market_data.get("LatestPrice")
        previous_close = market_data.get("Open") if market_type == 'otc' else market_data.get("PreviousAveragePrice")

        # 確保 current_price 和 previous_close 為數字格式
        try:
            current_price = float(current_price) if current_price not in [None, "N/A"] else "N/A"
            previous_close = float(previous_close) if previous_close not in [None, "N/A"] else "N/A"
        except ValueError:
            current_price = "N/A"
            previous_close = "N/A"

        if current_price != "N/A" and previous_close != "N/A":
            try:
                change = round(current_price - previous_close, 2)
                change_percent = round((change / previous_close) * 100, 2)
            except ZeroDivisionError:
                change = 0.0
                change_percent = 0.0
        else:
            change = "N/A"
            change_percent = "N/A"

        # 加入變動值和變動百分比到 market_data 字典中
        market_data["change"] = change
        market_data["changePercent"] = change_percent      

        for key, value in market_data.items():
            if value is None:
                market_data[key] = 'N/A'

    else:
        market_data = {}

    return market_data
