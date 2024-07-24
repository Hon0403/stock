from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date
from exts import db
from bcrypt import hashpw, gensalt, checkpw  # 導入 bcrypt 相關函數

class Members(UserMixin, db.Model):
    __tablename__ = 'Members'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    birthday = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    password_hash = Column(String(128), nullable=False)  # 新增的欄位

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, raw_password):
        salt = gensalt()
        self.password_hash = hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        return checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def get_id(self):
        return str(self.user_id)
    
    @property
    def is_active(self):
        return True  # 保持帳戶始終有效

    def __repr__(self):
        return f'<Member {self.user_name}>'
