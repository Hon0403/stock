# apps/fastapi/tpex_all_api/tpex_basic_info/tpex_basic_info.py

import json
import requests
import re  # 添加這行來導入 re 模組
from typing import Optional, Dict

def fetch_tpex_mainboard_basic_info() -> Optional[Dict]:
    """
    從 TPEX 主板基本資料 API 獲取資料。

    Returns:
        dict: 從 API 獲取的資料。
    """
    url = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"
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

def fetch_tpex_esm_basic_info() -> Optional[Dict]:
    """
    從 TPEX ESM 基本資料 API 獲取資料。

    Returns:
        dict: 從 API 獲取的資料。
    """
    url = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_R"
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

def get_company_data(market_code: str, market_type: str) -> dict:
    """
    根據市場類型和市場代碼獲取並處理公司資料。

    Args:
        market_code (str): 公司的市場代碼。
        market_type (str): 市場類型，'otc' 或 'esm'。

    Returns:
        dict: 處理過的公司資料。
    """
    data = None
    if market_type == 'otc':
        try:
            data = fetch_tpex_mainboard_basic_info()
        except RuntimeError as e:
            raise RuntimeError(f"獲取 OTC 資料時發生錯誤: {e}")
    elif market_type == 'esm':
        try:
            data = fetch_tpex_esm_basic_info()
        except RuntimeError as e:
            raise RuntimeError(f"獲取 ESM 資料時發生錯誤: {e}")
    else:
        raise ValueError("無效的市場類型")

    # 確保 data 是一個列表
    if not isinstance(data, list):
        raise ValueError("獲取的數據格式錯誤")

    # 根據 market_code 篩選單一公司資料
    company_data = next((item for item in data if item.get("SecuritiesCompanyCode") == market_code), None)
    
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
        
        # 轉換為 JSON 字符串
        company_data = json.loads(company_data_str)
        
        return company_data
    else:
        return {}
