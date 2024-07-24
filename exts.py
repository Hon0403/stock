# exts.py
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
import logging


db = SQLAlchemy()

# 主系統資料庫
main_engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=3600, pool_pre_ping=True)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
