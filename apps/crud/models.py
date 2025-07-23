from datetime import datetime
from apps.app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """SQLUserモデル
    table:users
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
    avg_score: float
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, nullable=False)
    email = db.Column(db.String, index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    avg_score = db.Column(db.Float, default=0.0)

    @property
    def password(self):
        raise AttributeError("読み取り不可")
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


# ログインしているユーザー情報を取得する関数を作成する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

