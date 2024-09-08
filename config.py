# config.py

import urllib
import os

# SQL Server連接設置
DATABASE_CONFIG = {
    'username': os.getenv('DB_USERNAME', 'sa'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': os.getenv('DB_PORT', '1433'),  # SQL Server的默認端口
    'database': os.getenv('DB_NAME', 'master'),
    'driver': 'ODBC Driver 17 for SQL Server'
}

# 將配置轉換為SQLAlchemy URI
params = urllib.parse.quote_plus(
    f"DRIVER={{{DATABASE_CONFIG['driver']}}};"
    f"SERVER={DATABASE_CONFIG['host']},{DATABASE_CONFIG['port']};"
    f"DATABASE={DATABASE_CONFIG['database']};"
    f"UID={DATABASE_CONFIG['username']};"
    f"PWD={DATABASE_CONFIG['password']}"
)

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"

# 其他配置
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    'pool_timeout': 900,
    'pool_size': 10,
    'max_overflow': 5,
}

# 基礎目錄
basedir = os.path.abspath(os.path.dirname(__file__))

# 如果您要使用 SQLite 而不是 SQL Server，則可以注釋掉以下兩行或修改為您的 SQLite 連接 URI
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.getenv('SECRET_KEY', 'dsgds135165gsdg')
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY', '91jSX8IiZ3RPEDcXnaUZ7LIFSdQou3eQ')
FUGLE_KEY = os.getenv('FUGLE_KEY', 'MWZhN2VmNWMtYTVkYi00ZDI5LTg5MDgtMTFmNTc1MTkzMGQ0IGJmNWFlYjk3LTJmMTItNDk1MS04NGVjLTkzMjVkNWNhNTk1Yw==')

