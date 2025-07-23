from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_key):
    app = Flask(__name__)
    app.config.from_object(config[config_key])
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    from apps.blogs import views as blogs_views
    app.register_blueprint(blogs_views.blogs, url_prefix="/blogs")
    return app
