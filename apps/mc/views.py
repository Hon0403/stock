# apps/mc/views.py

# 漲跌停還沒寫完 #

from math import ceil
import os
import requests
from flask import (
    jsonify,
    make_response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from flask_login import login_user, logout_user, login_required
from apps.fastapi.tpex_all_api.tpex_all_quotes.tpex_all_quotes import fetch_tpex_mainboard_quotes, fetch_tpex_esm_latest_statistics, process_market_data
from apps.fastapi.tpex_all_api.tpex_basic_info.tpex_basic_info import get_company_data
from apps.fastapi.twse_listed_info.twse_listed_info import get_twse_company_data  # 導入 get_twse_company_data 函數
from apps.mc.models import Members
from .api_requests import fetch_news_data, fetch_limit_up_data, fetch_limit_down_data
from . import bp
import pandas as pd
import yfinance as yf
from apps.stock_crawlers.fetch_yahoo_finance import fetch_yahoo_finance
import json
import csv
import datetime
import logging
import config


# 設置日誌配置
logging.basicConfig(level=logging.INFO)


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



def is_data_up_to_date(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            if rows:
                latest_date_str = rows[0]['Date']  # 取第一條數據行的日期
                logging.info(f"Latest date string: {latest_date_str}")  # 調試信息
                try:
                    latest_date = datetime.datetime.strptime(latest_date_str, '%b %d, %Y')  # 根據資料格式解析日期
                    logging.info(f"Latest date: {latest_date}")  # 調試信息
                    current_date = datetime.datetime.now()
                    logging.info(f"Current date: {current_date}")  # 調試信息
                    if (current_date - latest_date).days <= 1:
                        logging.info("Data is up to date.")
                        return True
                    else:
                        logging.info("Data is not up to date.")
                except ValueError as ve:
                    logging.error(f"日期解析錯誤: {ve}")
    except Exception as e:
        logging.error(f"檢查資料更新日期時發生錯誤: {e}")
    return False



@bp.route("/search_keywords")
def search_keywords():
    keyword = request.args.get("keyword", "").strip()
    
    if keyword:
        otc_stocks = []
        esm_stocks = []
        
        # 讀取 CSV 文件
        with open('apps/stock_crawlers/data/otc_stocks.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                otc_stocks.append(row)
        
        with open('apps/stock_crawlers/data/esm_stocks.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                esm_stocks.append(row)

        # 定義函數來判斷股票代號並添加後綴
        def add_suffix(market_code, otc_stocks, esm_stocks):
            if market_code in [stock['股票代號'] for stock in otc_stocks]:
                return market_code + '.TWO', 'otc'
            elif market_code in [stock['股票代號'] for stock in esm_stocks]:
                return market_code + '.TWO', 'esm'
            else:
                return None, None

        ticker, market_type = add_suffix(keyword, otc_stocks, esm_stocks)
        if ticker:
            original_ticker = ticker  # 保存原始的 ticker 值
            
            # 刪除 ticker 中的 .TWO
            if ".TWO" in ticker:
                ticker = ticker.replace(".TWO", "")
            
            file_path = os.path.join('apps', 'data', 'historical_data', f"{ticker}.csv")
            if os.path.exists(file_path) and is_data_up_to_date(file_path):
                print(f"{original_ticker} 的資料已經存在且是最新的，直接讀取資料。")
            else:
                fetch_yahoo_finance(original_ticker)  # 使用原始的 ticker 值
            
            # 設置 Cookie 並重定向
            response = make_response(redirect(url_for("mc.otc_esm_data", market_code=ticker, market_type=market_type)))
            response.set_cookie('market_code', ticker)  # 將 market_code 存入 Cookie
            response.set_cookie('market_type', market_type)  # 將 market_type 存入 Cookie
            logging.info(f"Redirecting to: {url_for('mc.otc_esm_data', market_code=ticker, market_type=market_type)}")
            return response
        else:
            # 如果找不到對應的代碼，重定向到 stock_data
            return redirect(url_for("mc.stock_data", stock_code=keyword))

    return redirect(url_for("mc.index"))



@bp.route("/stock_data", methods=["GET"])
@login_required
def stock_data():
    try:
        # 設定股票代碼        
        stock_code = request.args.get("stock_code", "")

        if not stock_code:
            return render_template(
                "mc/stock_data.html",
                error="請輸入股票代碼",
                stock_data={},
                stock_info={},
                listed_info={}
            )

        # 將股票代碼轉換為 Yahoo Finance 使用的格式
        ticker = f"{stock_code}.TW"  # 台股代碼後面加上 ".TW"

        # 創建股票對象
        stock = yf.Ticker(ticker)

        # 獲取即時行情數據
        stock_info = stock.info
        stock_history = stock.history(period="1d")

        # 計算變動值和變動百分比
        current_price = stock_info.get("currentPrice", "N/A")
        previous_close = stock_info.get("previousClose", "N/A")
        if current_price != "N/A" and previous_close != "N/A":
            try:
                change = round(float(current_price) - float(previous_close), 2)
                change_percent = round((change / float(previous_close)) * 100, 2)
                current_price = round(float(current_price), 2)
            except ValueError:
                change = "N/A"
                change_percent = "N/A"
        else:
            change = "N/A"
            change_percent = "N/A"

        # 計算成交量（張）和成交值（元）
        trading_volume_in_lots = (
            stock_history["Volume"].iloc[0] / 1000
            if "Volume" in stock_history.columns and not pd.isnull(stock_history["Volume"].iloc[0])
            else "N/A"
        )
        transaction_amount = (
            stock_history["Volume"].iloc[0] * stock_history["Close"].iloc[0]
            if "Volume" in stock_history.columns and "Close" in stock_history.columns
            and not pd.isnull(stock_history["Volume"].iloc[0]) and not pd.isnull(stock_history["Close"].iloc[0])
            else "N/A"
        )

        # 提取需要顯示的數據
        stock_data = {
            "code": stock_code,
            "name": stock_info.get("shortName", "N/A"),
            "price": f"{current_price:.2f}" if current_price != "N/A" else "N/A",
            "change": f"{change:.2f}" if change != "N/A" else "N/A",
            "changePercent": f"{change_percent:.2f}" if change_percent != "N/A" else "N/A",
            "date": stock_history.index[-1].strftime("%Y-%m-%d") if not stock_history.empty else "N/A",
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
            "trading_volume_in_lots": trading_volume_in_lots,
            "transaction_amount": transaction_amount,
        }

        # 獲取上市公司基本資料
        listed_info = get_twse_company_data(stock_code)
        print("listed_info", listed_info)
        
        # 檢查並處理 None 值
        listed_info = {key: (value if value is not None else 'N/A') for key, value in listed_info.items()}

        # 將 stock_info 轉換為 JSON 字符串
        try:
            stock_info_json = json.dumps(stock_info, ensure_ascii=False)
        except (TypeError, OverflowError) as e:
            print(f"Error serializing stock_info: {e}")
            stock_info_json = "{}"

        # 渲染模板
        return render_template(
            "mc/stock_data.html",
            stock_data=stock_data,
            stock_info=stock_info_json,
            stock_code=stock_code,
            listed_info=listed_info,
            basic_info={}
        )

    except Exception as e:
        import traceback
        print("An error occurred:", traceback.format_exc())
        return render_template(
            "mc/stock_data.html",
            error="發生錯誤: " + str(e),
            stock_data={},
            stock_info={},
            stock_code={},
            listed_info={},
            basic_info={}
        )





@bp.route("/otc_esm_data", methods=["GET"])
@login_required
def otc_esm_data():
    import re
    market_code = request.args.get("market_code", "")
    market_type = request.args.get("market_type", "")
    
    if not market_code or not market_type:
        return redirect(url_for("mc.index"))

    # 變數初始化
    data = None
    basic_info = None
    error_message = None

    # 獲取市場數據
    try:
        if market_type == 'otc':
            data = fetch_tpex_mainboard_quotes(market_code)
        elif market_type == 'esm':
            data = fetch_tpex_esm_latest_statistics(market_code)
        else:
            return redirect(url_for("mc.index"))
    except RuntimeError as e:
        error_message = f"獲取市場數據時發生錯誤: {e}"

    # 獲取基本資訊
    try:
        basic_info = get_company_data(market_code, market_type)
    except RuntimeError as e:
        error_message = f"獲取基本資訊時發生錯誤: {e}"
        print(error_message)
    except json.JSONDecodeError as e:
        # 處理 JSON 編碼錯誤
        print(f"JSON 編碼錯誤: {e}")

    if data:
        # 根據 market_type 處理市場數據
        market_data = process_market_data(data, market_code, market_type)
        # 返回渲染模板
        response = make_response(render_template(
            "mc/stock_data.html",
            market_data=market_data,
            stock_data={},
            basic_info=basic_info,  # 傳遞基本資訊
            market_code=market_code,
            market_type=market_type,
            listed_info=json.dumps(get_twse_company_data(market_code))  # 確保這裡是 JSON 可序列化的            
        ))
        response.set_cookie('market_code', market_code)  # 設置 Cookie
        return response

    # 如果沒有獲取到市場數據或發生錯誤
    response = make_response(render_template(
        "mc/stock_data.html",
        error=error_message or "無法獲取資料",  # 提供錯誤信息
        market_data=None,
        stock_data={},
        basic_info=basic_info,  # 即使市場數據錯誤，仍顯示基本資訊
        market_code=market_code,
        market_type=market_type,
        listed_info=json.dumps(get_twse_company_data(market_code))  # 確保這裡是 JSON 可序列化的
    ))
    response.set_cookie('market_code', market_code)  # 設置 Cookie
    return response





# 處理上市資料並建立k線圖
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

        if k_line_data is None:
            k_line_data = []
        print('上市資料:'+ str(clean_k_line_data))

        return jsonify({"k_line_data": clean_k_line_data, "stock_code": stock_code})

    except Exception as e:
        logging.error(f"Error fetching K-line data: {e}")
        return jsonify({"error": str(e)}), 500


# 建立興櫃和上櫃k線圖
@bp.route("/otc_k_line_data", methods=["GET"])
def otc_k_line_data():
    try:
        market_code = request.cookies.get('market_code')
        if not market_code:
            return jsonify({"error": "缺少 market_code 参数"}), 400

        csv_file_path = os.path.join('apps', 'data', 'historical_data', f"{market_code}.csv")

        if not os.path.isfile(csv_file_path):
            return jsonify({"error": "文件不存在"}), 404

        # 读取 CSV 文件，跳过第一行并处理列名
        market_data = pd.read_csv(csv_file_path, encoding='utf-8-sig', skiprows=0)

        # 確保列名正確
        column_rename_mapping = {
            'Date': 'Date',
            'Open': 'Open',
            'High': 'High',
            'Low': 'Low',
            'Close': 'Close'
        }

        # 重命名列名
        market_data.rename(columns=column_rename_mapping, inplace=True)

        # 处理日期和排序（日期从最新到最旧，需转换为升序）
        market_data['Date'] = pd.to_datetime(market_data['Date'], format='%b %d, %Y')
        market_data = market_data.sort_values('Date', ascending=True)

        market_data = market_data.dropna()  # 刪除包含 NaN 的行

        # 时间范围映射
        interval_mapping = {
            "1m": "1min", "2m": "2min", "5m": "5min", "15min": "15min",
            "30min": "30min", "60min": "60min", "90min": "90min", "1h": "1H",
            "1d": "1D", "5d": "5D", "1wk": "1W", "1mo": "1M",
            "3mo": "3M"
        }

        # 获取并转换时间范围
        k_line_range = request.args.get("k_line_ranges", "1d")
        interval = interval_mapping.get(k_line_range, "1D")

        if interval in ["1min", "2min", "5min", "15min", "30min", "60min", "90min", "1H"]:
            market_data = market_data.resample(interval, on='Date').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last'
            }).dropna().reset_index()

        k_line_data = market_data[['Date', 'Open', 'High', 'Low', 'Close']].to_dict(orient='records')

        clean_k_line_data = [
            {
                'Date': int(record['Date'].timestamp() * 1000),
                'Open': record['Open'] if pd.notna(record['Open']) else None,
                'High': record['High'] if pd.notna(record['High']) else None,
                'Low': record['Low'] if pd.notna(record['Low']) else None,
                'Close': record['Close'] if pd.notna(record['Close']) else None
            }
            for record in k_line_data
        ]

        print('otc資料:', clean_k_line_data)
        return jsonify({"otc_k_line_data": clean_k_line_data})

    except Exception as e:
        logging.error(f"Error fetching K-line data from CSV: {e}")
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



@bp.route("/fugle_tickers", methods=["GET"])
@login_required
def fugle_tickers():
    from fugle_marketdata import RestClient
    client = RestClient(api_key=config.FUGLE_KEY)
    stock = client.stock
    response = stock.intraday.tickers(type='EQUITY', exchange="TWSE", industry="24", isNormal=True)
    print(response)
    return jsonify(response)  # 返回 JSON 格式的回應
