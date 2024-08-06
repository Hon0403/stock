# apps/fastapi/stock_day_api/stock_day_api.py

from fastapi import APIRouter, HTTPException
from typing import List
import httpx
from pydantic import BaseModel

router = APIRouter()

# API URLs
API_URLS = {
    "stock_day": "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",
    "monthly": "https://openapi.twse.com.tw/v1/exchangeReport/FMSRFK_ALL",
    "yearly": "https://openapi.twse.com.tw/v1/exchangeReport/FMNNPTK_ALL",
}

class StockDayData(BaseModel):
    Code: str
    Name: str
    TradeVolume: str
    TradeValue: str
    OpeningPrice: str
    HighestPrice: str
    LowestPrice: str
    ClosingPrice: str
    Change: str
    Transaction: str

class MonthlyData(BaseModel):
    Code: str
    Name: str
    HighestPrice: str
    LowestPrice: str
    WeightedAvgPriceAB: str
    Transaction: str
    TradeValueA: str
    TradeVolumeB: str
    TurnoverRatio: str

class YearlyData(BaseModel):
    Code: str
    Name: str
    TradeVolume: str
    TradeValue: str
    Transaction: str
    HighestPrice: str
    HDate: str
    LowestPrice: str
    LDate: str
    AvgClosingPrice: str

async def fetch_data(api_url: str) -> List[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        response.raise_for_status()
        return response.json()

@router.get("/api/stock_day", response_model=List[StockDayData])
async def read_stock_day():
    json_data = await fetch_data(API_URLS["stock_day"])
    if isinstance(json_data, list):
        return [StockDayData(**item) for item in json_data]
    raise HTTPException(status_code=500, detail="Unexpected data format")

@router.get("/api/monthly", response_model=List[MonthlyData])
async def read_monthly():
    json_data = await fetch_data(API_URLS["monthly"])
    if isinstance(json_data, list):
        return [MonthlyData(**item) for item in json_data]
    raise HTTPException(status_code=500, detail="Unexpected data format")

@router.get("/api/yearly", response_model=List[YearlyData])
async def read_yearly():
    json_data = await fetch_data(API_URLS["yearly"])
    if isinstance(json_data, list):
        return [YearlyData(**item) for item in json_data]
    raise HTTPException(status_code=500, detail="Unexpected data format")