# apps/fastapi/news_api/news_requests.py
import aiohttp
from fastapi import APIRouter, HTTPException

router = APIRouter()

BASE_URL = "https://openapi.twse.com.tw/v1"

async def fetch_data(endpoint: str):
    url = BASE_URL + endpoint
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data from {url}")
        except ValueError as e:
            raise HTTPException(status_code=500, detail=f"Error decoding JSON from {url}")

@router.get("/opendata/t187ap04_L")
async def get_daily_important_news():
    return await fetch_data('/opendata/t187ap04_L')

@router.get("/opendata/t187ap38_L")
async def get_shareholders_meeting_news():
    return await fetch_data('/opendata/t187ap38_L')

@router.get("/announcement/notice")
async def get_market_notice_news():
    return await fetch_data('/announcement/notice')

@router.get("/announcement/notetrans")
async def get_market_abnormal_info_news():
    return await fetch_data('/announcement/notetrans')