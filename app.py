# app.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
import config
from utils.jinja_tester import check_oper
from apps.mc import init_app, bp
from apps.mc.models import Members
from exts import db


def create_app():
    app = Flask(__name__)  # 指定模板文件夾的路徑
    app.config.from_object(config)
    app.config['STATIC_FOLDER'] = 'static'

    # 初始化插件
    db.init_app(app)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)

    # 設置登錄管理器
    login_manager = LoginManager()
    login_manager.login_view = 'mc.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with db.session() as session:  # 使用 db.session() 获取数据库会话
            return session.get(Members, int(user_id))  # 使用 Session.get 方法获取用户对象

    # 註冊藍圖
    init_app(app)
    # 引入自定義測試器
    app.add_template_test(check_oper, 'jinja_check_oper')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(threaded=True, debug=True, port=5000)

