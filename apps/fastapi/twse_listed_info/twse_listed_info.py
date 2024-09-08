#apps\fastapi\twse_listed_info\twse_listed_info.py

import requests
import json
import re
from typing import Optional, Dict

def fetch_twse_listed_info() -> Optional[Dict]:
    """
    從 TWSE 上市公司基本資料 API 獲取資料。

    Returns:
        dict: 從 API 獲取的資料。
    """
    url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f"HTTP 狀態碼錯誤: {response.status_code}")
    except requests.RequestException as e:
        raise RuntimeError(f"網路錯誤: {e}")

def get_twse_company_data(company_code: str) -> dict:
    """
    根據公司代碼獲取並處理 TWSE 上市公司資料。

    Args:
        company_code (str): 公司的代碼。

    Returns:
        dict: 處理過的公司資料。
    """
    data = fetch_twse_listed_info()

    # 確保 data 是一個列表
    if not isinstance(data, list):
        raise ValueError("獲取的數據格式錯誤")

    # 根據 company_code 篩選單一公司資料
    company_data = next((item for item in data if item.get("公司代號") == company_code), None)

    if company_data:
        # 檢查並處理 undefined 或 None 值
        company_data = {key: (value if value is not None else 'N/A') for key, value in company_data.items()}

        # 移除特殊字符
        company_data_str = json.dumps(company_data, ensure_ascii=False, indent=4)
        company_data_str = re.sub(r'[\n\t]', '', company_data_str)
        
        # 修改屬性名稱
        company_data_str = company_data_str.replace('Paidin.Capital.NTDollars', 'PaidinCapitalNTDollars')
        company_data_str = company_data_str.replace('PrivateStock.shares', 'PrivateStockShares')
        company_data_str = company_data_str.replace('PreferredStock.shares', 'PreferredStockShares')
        company_data_str = company_data_str.replace('CPA.CharteredPublicAccountant.First', 'CPACharteredPublicAccountantFirst')
        company_data_str = company_data_str.replace('CPA.CharteredPublicAccountant.Second', 'CPACharteredPublicAccountantSecond')

        # 將處理後的字串轉回字典
        company_data = json.loads(company_data_str)
        
        return company_data
    else:
        return {}
