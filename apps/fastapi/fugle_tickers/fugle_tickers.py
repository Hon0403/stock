# apps\fastapi\fugle_tickers\fugle_tickers.py
from fastapi import FastAPI
import requests
from config import FUGLE_KEY



app = FastAPI()

@app.get("/intraday/tickers")
def get_tickers():
    url = "https://api.fugle.tw/marketdata/v1.0/stock/intraday/tickers"
    params = {
        "type": "EQUITY",
        "exchange": "TWSE",
        "isNormal": "true"
    }
    headers = {
        "X-API-KEY": FUGLE_KEY
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()
