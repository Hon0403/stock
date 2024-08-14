# apps/mc/views.py

# 漲跌停還沒寫完 #

import asyncio
from asyncio.log import logger
from math import ceil
import httpx
import requests
from flask import (
    Blueprint,
    jsonify,
    logging,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from flask_login import login_user, logout_user, login_required
from apps.fastapi.stock_data_api.stock_data_api import API_URLS
from apps.mc.models import Members
from apps.fastapi.news_api.news_requests import fetch_data  # 確保這是正確的導入
from .api_requests import fetch_news_data, fetch_limit_up_data, fetch_limit_down_data
from . import bp
from datetime import datetime
import pandas as pd
import yfinance as yf


@bp.route("/")
@login_required
def index():
    try:

        # 處理公告 #

        endpoints = {
            "daily_important": "opendata/t187ap04_L",
            "shareholders_meeting": "opendata/t187ap38_L",
            "market_notice": "announcement/notice",
            "market_abnormal": "announcement/notetrans",
        }

        news_data = fetch_news_data(endpoints)
        limit_up_data = fetch_limit_up_data()
        limit_down_data = fetch_limit_down_data()

        daily_important_more_url = url_for(
            "mc.index", _external=True, endpoint_name="daily_important"
        )
        shareholders_meeting_more_url = url_for(
            "mc.index", _external=True, endpoint_name="shareholders_meeting"
        )
        market_notice_more_url = url_for(
            "mc.index", _external=True, endpoint_name="market_notice"
        )
        market_abnormal_more_url = url_for(
            "mc.index", _external=True, endpoint_name="market_abnormal"
        )

        return render_template(
            "mc/index.html",
            news_data=news_data,
            error=None,
            daily_important_more_url=daily_important_more_url,
            shareholders_meeting_more_url=shareholders_meeting_more_url,
            market_notice_more_url=market_notice_more_url,
            market_abnormal_more_url=market_abnormal_more_url,
            price_limits=limit_up_data,
            limit_down_data=limit_down_data,
        )

    except Exception as e:
        current_app.logger.error(f"Error fetching news data: {str(e)}")
        return render_template("mc/index.html", news_data=None, error=str(e))


@bp.route("/login", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        current_app.logger.info("Login form submitted")
        user_id = request.form["user_id"]
        password = request.form["password"]

        user = Members.query.filter_by(user_id=user_id).first()

        if user and user.check_password(password):
            login_user(user)
            flash("登入成功", "success")
            return redirect(url_for("mc.index"))
        else:
            message = "用戶ID或密碼錯誤"
            flash(message, "error")

    return render_template("mc/login.html", message=message)


@bp.route("/logout")
@login_required
def logout():
    current_app.logger.info("Logout page accessed")
    logout_user()
    flash("您已成功登出。", "info")
    return redirect(url_for("mc.login"))


@bp.route("/forget_password")
def forget_password():
    current_app.logger.info("Forget password page accessed")
    # 添加忘记密码逻辑
    return render_template("mc/forget_password.html")


@bp.route("/news")
@login_required
def news():
    section = request.args.get("section", "daily_important")
    page = request.args.get("page", 1, type=int)
    per_page = 10  # 每页显示10条数据

    endpoints = {
        "daily_important": "opendata/t187ap04_L",
        "shareholders_meeting": "opendata/t187ap38_L",
        "market_notice": "announcement/notice",
        "market_abnormal": "announcement/notetrans",
    }

    url = endpoints.get(section)
    if url:
        try:
            response = requests.get(f"https://openapi.twse.com.tw/v1/{url}")
            response.raise_for_status()
            all_news_data = response.json()

            # 数据分页处理
            total_count = len(all_news_data)
            total_pages = max(
                (total_count + per_page - 1) // per_page, 1
            )  # 确保至少为1
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            news_data = all_news_data[start_index:end_index]

            template_map = {
                "daily_important": "mc/daily_important.html",
                "shareholders_meeting": "mc/shareholders_meeting.html",
                "market_notice": "mc/market_notice.html",
                "market_abnormal": "mc/market_abnormal.html",
            }

            template = template_map.get(section, "mc/index.html")

            return render_template(
                template,
                news_data=news_data,
                error=None,
                daily_important_more_url=url_for("mc.news", section="daily_important"),
                shareholders_meeting_more_url=url_for(
                    "mc.news", section="shareholders_meeting"
                ),
                market_notice_more_url=url_for("mc.news", section="market_notice"),
                market_abnormal_more_url=url_for("mc.news", section="market_abnormal"),
                total_pages=total_pages,
                current_page=page,
                section=section,
            )
        except Exception as e:
            current_app.logger.error(f"Error fetching news data: {str(e)}")
            return render_template("mc/index.html", news_data=None, error=str(e))
    # 如果没有指定的 section，返回首页数据
    return redirect(url_for("mc.news", section="daily_important", page=1))


@bp.route("/price_limits")
@login_required
def price_limits():

    Code = request.args.get("Code", "AAPL")  # 默認股票代碼為 'AAPL'

    try:
        response = requests.get(
            f"http://127.0.0.1:8000/price-limits/api/stocks/{Code}"
        )  # 替換為你的 FastAPI 服務地址
        response.raise_for_status()
        price_limits_data = response.json()

        return render_template("index.html", price_limits=price_limits_data)
    except requests.HTTPError as e:
        current_app.logger.error(f"HTTP error fetching price limits: {str(e)}")
        return render_template("index.html", price_limits=None, error=str(e))
    except Exception as e:
        current_app.logger.error(f"Error fetching price limits: {str(e)}")
        return render_template("index.html", price_limits=None, error=str(e))


@bp.route("/search_keywords")
def search_keywords():
    keyword = request.args.get("keyword", "")

    if keyword:
        return redirect(url_for("mc.stock_data", stock_code=keyword))

    return redirect(url_for("mc.index"))


@bp.route("/stock_data", methods=["GET"])
@login_required
def stock_data():

    # 初始化最後修改時間的變數
    formatted_last_modified = None

    try:
        # 設定股票代碼
        stock_code = request.args.get("stock_code", "")
        if not stock_code:
            return render_template(
                "mc/stock_data.html",
                error="請輸入股票代碼",
                stock_data=None,
                last_modified=formatted_last_modified,
            )

        # 將股票代碼轉換為 Yahoo Finance 使用的格式
        ticker = f"{stock_code}.TW"  # 台股代碼後面加上 ".TW"

        # 創建股票對象
        stock = yf.Ticker(ticker)

        # 獲取即時行情數據
        stock_info = stock.info
        stock_history = stock.history(period="1d")

        # 格式化最後修改時間
        last_modified_datetime = stock_history.index[-1]
        formatted_last_modified = last_modified_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # 提取需要顯示的數據
        stock_data = {
            "code": stock_code,
            "name": stock_info.get("shortName", "N/A"),
            "price": stock_info.get("currentPrice", "N/A"),
            "change": stock_info.get("dayChange", "N/A"),
            "changePercent": stock_info.get("dayChangePercent", "N/A"),
            "volume": (
                int(stock_history["Volume"].iloc[0])
                if "Volume" in stock_history.columns
                and not pd.isnull(stock_history["Volume"].iloc[0])
                else "N/A"
            ),
            "open": (
                stock_history["Open"].iloc[0]
                if "Open" in stock_history.columns
                and not pd.isnull(stock_history["Open"].iloc[0])
                else "N/A"
            ),
            "close": (
                stock_history["Close"].iloc[0]
                if "Close" in stock_history.columns
                and not pd.isnull(stock_history["Close"].iloc[0])
                else "N/A"
            ),
            "high": (
                stock_history["High"].iloc[0]
                if "High" in stock_history.columns
                and not pd.isnull(stock_history["High"].iloc[0])
                else "N/A"
            ),
            "low": (
                stock_history["Low"].iloc[0]
                if "Low" in stock_history.columns
                and not pd.isnull(stock_history["Low"].iloc[0])
                else "N/A"
            ),
            "sector": stock_info.get("sector", "N/A"),
            "industry": stock_info.get("industry", "N/A"),
            "country": stock_info.get("country", "N/A"),
            "employees": stock_info.get("fullTimeEmployees", "N/A"),
            "ceo": stock_info.get("ceo", "N/A"),
        }

        # 這裡我們移除了 k_line_data 的處理

        return render_template(
            "mc/stock_data.html",
            stock_data=stock_data,
            last_modified=formatted_last_modified,
            stock_info=stock_info,
        )

    except Exception as e:
        return render_template(
            "mc/stock_data.html",
            error=str(e),
            stock_data=None,
            last_modified=formatted_last_modified,
            stock_info={},
        )


@bp.route("/k_line_data", methods=["GET"])
@login_required
def kline_data():
    try:
        stock_code = request.args.get("stock_code", "")
        k_line_range = request.args.get("k_line_ranges")  # 获取时间范围参数

        ticker = f"{stock_code}.TW"
        stock = yf.Ticker(ticker)

        # 定义时间间隔映射
        interval_mapping = {
            "1m": "1m",  # 1 分鐘
            "2m": "2m",  # 2 分鐘
            "5m": "5m",  # 5 分鐘
            "15m": "15m",  # 15 分鐘
            "30m": "30m",  # 30 分鐘
            "60m": "60m",  # 60 分鐘
            "90m": "90m",  # 90 分鐘
            "1h": "1h",  # 1 小時
            "1d": "1d",  # 1 天
            "5d": "5d",  # 5 天
            "1wk": "1wk",  # 1 週
            "1mo": "1mo",  # 1 個月
            "3mo": "3mo",  # 3 個月
        }

        # 获取相应的时间间隔
        interval = interval_mapping.get(k_line_range)

        # 判斷是否為兩分鐘間隔
        if interval == "2m":
            period = "1mo"  # 只撈取最近 60 天的數據
        else:
            period = "max"  # 按照原本的邏輯處理

        # 获取历史数据
        stock_history = stock.history(
            period=period,
            interval=interval,
            start=None,
            end=None,
            actions=True,
            auto_adjust=True,
            back_adjust=False,
        )


        k_line_data = stock_history.reset_index().to_dict(orient="records")

        clean_k_line_data = [
            {
                k: (v if v is not None and not pd.isna(v) else None)
                for k, v in record.items()
            }
            for record in k_line_data
        ]

        logger.info(f"Generated K-Line data: {clean_k_line_data}")

        if k_line_data is None:
            k_line_data = []

        return jsonify({"k_line_data": clean_k_line_data, "stock_code": stock_code})

    except Exception as e:
        logging.error(f"Error fetching K-line data: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route("/api/weighted_index", methods=["GET"])
@login_required
def api_weighted_index():
    try:
        ticker = "^TWII"
        index = yf.Ticker(ticker)
        hist = index.history(period="1mo")
        weighted_index_data = hist.reset_index().to_dict(orient="records")

        # 打印調試信息
        current_app.logger.info(f"Weighted index data: {weighted_index_data}")

        return jsonify(weighted_index_data)
    except Exception as e:
        current_app.logger.error(f"Error fetching weighted index data: {str(e)}")
        return jsonify({"error": str(e)}), 500
