import logging as log
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config

db = SQLAlchemy()

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

log.basicConfig(
    level=log.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

handler = RotatingFileHandler(
    "app.log", maxBytes=10000, backupCount=1
)
handler.setLevel(log.DEBUG)
log.getLogger().addHandler(handler)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    print(f'config_name: {config_name}')
    print(f'config[config_name]: {config[config_name]}')
    print(f'config[config_name].SQLALCHEMY_DATABASE_URI: {config[config_name].SQLALCHEMY_DATABASE_URI}')

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.general.general import general_bp
    from app.auth.auth import auth_bp
    from app.api.table_data import api_bp
    from app.annotation_table.annotation_table import table_bp

    app.register_blueprint(general_bp, url_prefix="/")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(table_bp, url_prefix="/table")

    return app
