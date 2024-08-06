# apps/fastapi/stock_day_api/main.py

from fastapi import FastAPI
from apps.fastapi.stock_data_api.stock_data_api import router as stock_day_api_router
from typing import Union


app = FastAPI()

app.include_router(stock_day_api_router, prefix="/stock-day")