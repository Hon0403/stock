# apps/fastapi/price_limits_api/price_limits.py

from fastapi import APIRouter, HTTPException
from typing import List, Union
import httpx
from pydantic import BaseModel

router = APIRouter()

API_URL = "https://openapi.twse.com.tw/v1/exchangeReport/TWT84U"

class StockData(BaseModel):
    Code: str
    Name: str
    TodayLimitUp: str
    TodayOpeningRefPrice: str
    TodayLimitDown: str
    PreviousDayOpeningRefPrice: str
    PreviousDayPrice: str
    PreviousDayLimitUp: str
    PreviousDayLimitDown: str
    LastTradingDay: str
    AllowOddLotTrade: str

class ErrorResponse(BaseModel):
    error: str

@router.get("/api/stocks", response_model=List[StockData])
async def read_all_stocks():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_URL)
            response.raise_for_status()  # 確保狀態碼是200

            data = response.json()

            if isinstance(data, list):
                return [StockData(**item) for item in data]
            else:
                raise HTTPException(status_code=500, detail={"error": "Unexpected data format: not a list"})

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail={"error": f"HTTP error: {str(e)}"})
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail={"error": f"Request error: {str(e)}"})
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error": f"Internal server error: {str(e)}"})
