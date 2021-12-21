import os
from os.path import join


BASEDIR = os.path.abspath(os.path.dirname(__file__))
DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
ROOT = os.path.dirname(os.path.realpath(__file__))

def create_sqlite_uri(db_name):
    return "sqlite:///" + join(BASEDIR, db_name)


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN = os.environ.get("EXACT_TOKEN_TYPES")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DB_NAME = os.environ.get("POSTGRES_DB")
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASS = os.environ.get("POSTGRES_PASSWORD")
    DB_HOST = os.environ.get("POSTGRES_HOST")
    DB_PORT = os.environ.get("POSTGRES_PORT")
    DEBUG = os.environ.get("DEBUG")


class DevelopmentConfig(Config):
    DEBUG = os.environ.get("DEBUG")
    DB_NAME = os.environ.get("POSTGRES_DB")
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASS = os.environ.get("POSTGRES_PASSWORD")
    DB_HOST = os.environ.get("POSTGRES_HOST")
    DB_PORT = os.environ.get("POSTGRES_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("test_todo.db")
    WTF_CSRF_ENABLED = False
