import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_PATH')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
