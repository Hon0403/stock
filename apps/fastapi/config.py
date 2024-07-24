# apps/fastapi/config.py

from fastapi import FastAPI

app = FastAPI(
    title='Stock Exchange News API',
    description='API to retrieve news from the stock exchange.',
    version='1.0.0',
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url='/api/redocs'
)
