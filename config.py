import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = 'dev-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/User/james portfolio/instance/portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    DEBUG = True

config = {
    'default': Config,
    'development': Config,
    'production': Config
}
