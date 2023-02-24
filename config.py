import os
import secrets

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = secrets.token_urlsafe(16)
    SESSION_COOKIE_SECURE = True

    SQL_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    ADMIN = os.environ.get("ADMIN")

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    if os.environ.get("DATABASE_URL") is not None:
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "app.db")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQL_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "app.db")


class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
