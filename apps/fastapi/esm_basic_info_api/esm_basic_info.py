# apps/fastapi/esm_basic_info_api/esm_basic_info.py

import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/esm_basic_info")
async def get_esm_basic_info():
    url = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_R"
    headers = {
        "accept": "application/json",
        "If-Modified-Since": "Mon, 26 Jul 1997 05:00:00 GMT",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果狀態碼不是200，將觸發HTTPError
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

