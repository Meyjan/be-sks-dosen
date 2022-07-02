import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABSE_URI = os.environ.get('DATABASE_URL') or 'mysql://root@localhost:3306/db-sks-dosen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False