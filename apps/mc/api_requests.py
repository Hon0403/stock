import requests
from flask import current_app

def fetch_news_data(endpoints):
    news_data = {}
    for key, url in endpoints.items():
        current_app.logger.info(f"Fetching data from {url}")
        response = requests.get(f"https://openapi.twse.com.tw/v1/{url}")
        response.raise_for_status()
        data = response.json()
        news_data[key] = data[:3]  # 只保留前三筆資料
        current_app.logger.info(f"Fetched data for {key}: {news_data[key]}")
    return news_data

def fetch_limit_up_data():
    try:
        response = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/TWT84U")
        response.raise_for_status()
        data = response.json()
        limit_up_data = [item for item in data if item.get('TodayLimitUp') == 'True']
        return limit_up_data
    except requests.HTTPError as e:
        current_app.logger.error(f"Error fetching limit up data: {str(e)}")
        return None
    except Exception as e:
        current_app.logger.error(f"Error fetching limit up data: {str(e)}")
        return None

def fetch_limit_down_data():
    try:
        response = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/TWT84U")
        response.raise_for_status()
        data = response.json()
        limit_down_data = [item for item in data if item.get('TodayLimitDown') == 'True']
        return limit_down_data
    except requests.HTTPError as e:
        current_app.logger.error(f"Error fetching limit down data: {str(e)}")
        return None
    except Exception as e:
        current_app.logger.error(f"Error fetching limit down data: {str(e)}")
        return None
