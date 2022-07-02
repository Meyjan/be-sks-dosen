import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'this_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQL_HOSTNAME = "localhost"
    SQL_DATABASE = "db-sks-dosen"
    SQL_USERNAME = "root"
    SQL_PASSWORD = ""
    SQL_URI = "mysql://root@localhost:3306/db-sks-dosen"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQL_HOSTNAME = "localhost"
    SQL_DATABASE = "db-sks-dosen"
    SQL_USERNAME = "root"
    SQL_PASSWORD = ""
    SQL_URI = "mysql://root@localhost:3306/db-sks-dosen"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    # Fill in with production if ready

config_by_name = dict(
    dev = DevelopmentConfig,
    test = TestingConfig,
    prod = ProductionConfig
)

key = Config.SECRET_KEY