# apps/fastapi/main.py

from fastapi import FastAPI
from apps.fastapi.price_limits_api.price_limits import router as price_limits_router
from typing import Union


app = FastAPI()

app.include_router(price_limits_router, prefix="/price-limits")

