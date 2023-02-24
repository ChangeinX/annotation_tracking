from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()

csrf = CSRFProtect()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object("config.{}".format(config_name))

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.api.table_data import api_bp
    from app.login.login import login_bp
    from app.annotation_table.annotation_table import table_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(login_bp, url_prefix="/login")
    app.register_blueprint(table_bp, url_prefix="/table")

    login_manager.login_view = "login.login"

    return app
