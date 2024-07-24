# apps/mc/__init__.py


from flask import Blueprint


bp = Blueprint('mc', __name__)

def init_app(app):
    from . import views  # 確保 views 被導入以註冊路由
    app.register_blueprint(bp, url_prefix='/mc')


