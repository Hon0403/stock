from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apps.fastapi.news_api.news_requests import fetch_data, router as news_router

app = FastAPI()

# 設定模板目錄
templates = Jinja2Templates(directory="templates")

# 設定靜態文件目錄
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含新聞路由器
app.include_router(news_router, prefix="/news")

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
