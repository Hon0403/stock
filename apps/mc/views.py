# apps/mc/views.py

from math import ceil
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from apps.mc.models import Members
from apps.fastapi.news_api.news_requests import fetch_data  # 確保這是正確的導入
from . import bp

@bp.route('/')
@login_required
def index():
    try:
        current_app.logger.info("Index page accessed")
        endpoints = {
            'daily_important': "opendata/t187ap04_L",
            'shareholders_meeting': "opendata/t187ap38_L",
            'market_notice': "announcement/notice",
            'market_abnormal': "announcement/notetrans"
        }

        news_data = {}
        for key, url in endpoints.items():
            current_app.logger.info(f"Fetching data from {url}")
            response = requests.get(f"https://openapi.twse.com.tw/v1/{url}")
            response.raise_for_status()
            data = response.json()
            news_data[key] = data[:3]  # 只保留前三筆資料
            current_app.logger.info(f"Fetched data for {key}: {news_data[key]}")

        daily_important_more_url = url_for('mc.index', _external=True, endpoint_name='daily_important')
        shareholders_meeting_more_url = url_for('mc.index', _external=True, endpoint_name='shareholders_meeting')
        market_notice_more_url = url_for('mc.index', _external=True, endpoint_name='market_notice')
        market_abnormal_more_url = url_for('mc.index', _external=True, endpoint_name='market_abnormal')

        return render_template(
            'mc/index.html',
            news_data=news_data,
            error=None,
            daily_important_more_url=daily_important_more_url,
            shareholders_meeting_more_url=shareholders_meeting_more_url,
            market_notice_more_url=market_notice_more_url,
            market_abnormal_more_url=market_abnormal_more_url
        )

    except Exception as e:
        current_app.logger.error(f"Error fetching news data: {str(e)}")
        return render_template('mc/index.html', news_data=None, error=str(e))



@bp.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info("Login page accessed")
    message = None

    if request.method == 'POST':
        current_app.logger.info("Login form submitted")
        user_id = request.form['user_id']
        password = request.form['password']

        user = Members.query.filter_by(user_id=user_id).first()

        if user and user.check_password(password):
            login_user(user)
            flash('登入成功', 'success')
            return redirect(url_for('mc.index'))
        else:
            message = '用戶ID或密碼錯誤'
            flash(message, 'error')

    return render_template('mc/login.html', message=message)

@bp.route('/logout')
@login_required
def logout():
    current_app.logger.info("Logout page accessed")
    logout_user()
    flash('您已成功登出。', 'info')
    return redirect(url_for('mc.login'))

@bp.route('/forget_password')
def forget_password():
    current_app.logger.info("Forget password page accessed")
    # 添加忘记密码逻辑
    return render_template('mc/forget_password.html')


@bp.route('/news')
@login_required
def news():
    section = request.args.get('section', 'daily_important')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示10条数据

    endpoints = {
        'daily_important': "opendata/t187ap04_L",
        'shareholders_meeting': "opendata/t187ap38_L",
        'market_notice': "announcement/notice",
        'market_abnormal': "announcement/notetrans"
    }
    
    url = endpoints.get(section)
    if url:
        try:
            current_app.logger.info(f"Fetching data from {url}")
            response = requests.get(f"https://openapi.twse.com.tw/v1/{url}")
            response.raise_for_status()
            all_news_data = response.json()
            
            # 数据分页处理
            total_count = len(all_news_data)
            total_pages = max((total_count + per_page - 1) // per_page, 1)  # 确保至少为1
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            news_data = all_news_data[start_index:end_index]

            template_map = {
                'daily_important': 'mc/daily_important.html',
                'shareholders_meeting': 'mc/shareholders_meeting.html',
                'market_notice': 'mc/market_notice.html',
                'market_abnormal': 'mc/market_abnormal.html'
            }
            
            template = template_map.get(section, 'mc/index.html')
            
            return render_template(
                template,
                news_data=news_data,
                error=None,
                daily_important_more_url=url_for('mc.news', section='daily_important'),
                shareholders_meeting_more_url=url_for('mc.news', section='shareholders_meeting'),
                market_notice_more_url=url_for('mc.news', section='market_notice'),
                market_abnormal_more_url=url_for('mc.news', section='market_abnormal'),
                total_pages=total_pages,
                current_page=page,
                section=section
            )
        except Exception as e:
            current_app.logger.error(f"Error fetching news data: {str(e)}")
            return render_template('mc/index.html', news_data=None, error=str(e))
    # 如果没有指定的 section，返回首页数据
    return redirect(url_for('mc.news', section='daily_important', page=1))




