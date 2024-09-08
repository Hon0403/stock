# apps/fastapi/main.py

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from apps.fastapi.config import app  # 使用 config.py 中的 app 實例
from apps.fastapi.stock_data_api.stock_data_api import router as stock_day_api_router
from apps.fastapi.price_limits_api.price_limits import router as price_limits_router
from apps.fastapi.otc_basic_info_api.otc_basic_info import router as otc_basic_info_router
from apps.fastapi.esm_basic_info_api.esm_basic_info import router as esm_basic_info_router
from apps.fastapi.psb_company_info_api.psb_company_info import router as psb_company_info_router
from apps.fastapi.news_api.news_requests import fetch_data, router as news_router
from apps.fastapi.tpex_all_api.tpex_all_quotes.tpex_all_quotes import router as tpex_mainboard_quotes_router

# 設定模板目錄
templates = Jinja2Templates(directory="templates")

# 設定靜態文件目錄
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含路由器
app.include_router(stock_day_api_router, prefix="/stock-day")
app.include_router(price_limits_router, prefix="/price-limits")
app.include_router(news_router, prefix="/news")
# 加入上櫃股票基本資料的路由
app.include_router(otc_basic_info_router, prefix="/api")
# 加入興櫃股票基本資料的路由
app.include_router(esm_basic_info_router, prefix="/api")
# 加入創櫃版公司資訊的路由
app.include_router(psb_company_info_router, prefix="/api")
# 加入上櫃股票收盤行情
app.include_router(tpex_mainboard_quotes_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        daily_important_news = await fetch_data('/opendata/t187ap04_L')
        shareholders_meeting_news = await fetch_data('/opendata/t187ap38_L')
        market_notice_news = await fetch_data('/announcement/notice')
        market_abnormal_info_news = await fetch_data('/announcement/notetrans')

        return templates.TemplateResponse("mc/index.html", {
            "request": request,
            "daily_important_news": daily_important_news,
            "shareholders_meeting_news": shareholders_meeting_news,
            "market_notice_news": market_notice_news,
            "market_abnormal_info_news": market_abnormal_info_news
        })
    except Exception as e:
        print(f"Error fetching news data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
