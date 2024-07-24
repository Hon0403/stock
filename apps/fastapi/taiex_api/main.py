from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import logging
from apps.fastapi.taiex_api.price_requests import get_exchange_price_list
from apps.fastapi.config import app


logging.basicConfig(level=logging.INFO)

# 配置 Jinja2 模板
templates = Jinja2Templates(directory="templates")

# 配置靜態文件路由
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        price_data = get_exchange_price_list()
        if not price_data:
            price_data = []  # 處理返回的數據為空的情況
        logging.info(f"Home page news data: {price_data}")
        return templates.TemplateResponse("mc/index.html", {"request": request, "price_data": price_data})
    except Exception as e:
        logging.error(f"Error processing home page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/price", response_class=HTMLResponse)
async def news_page(request: Request):
    try:
        price_data = get_exchange_price_list()
        if not price_data:
            price_data = []
        logging.info(f"News page news data: {price_data}")
        return templates.TemplateResponse("mc/price.html", {"request": request, "price_data": price_data})
    except Exception as e:
        logging.error(f"Error processing news page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
