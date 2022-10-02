
import os
import sys
from dotenv import load_dotenv

load_dotenv('.env')

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

BASEDIR = os.path.abspath(os.path.dirname(__file__))
def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(BASEDIR, db_name)

class Operators:
    def __init__(self):
        pass

    RESET_PASSWORD = 'reset-password'


class BaseConfig:
    # Paginate configure
    BLOGIN_BLOG_PER_PAGE = 8
    BLOGIN_COMMENT_PER_PAGE = 10
    BLOGIN_PHOTO_PER_PAGE = 12
    LOGIN_LOG_PER_PAGE = 20
    SECRET_KEY = os.getenv('SECRET_KEY')
    JSON_AS_ASCII = False
    BLOGIN_MAIL_SUBJECT_PRE = '[Blogin]'

    # CKEditor configure
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_HEIGHT = 500
    CKEDITOR_CODE_THEME = 'docco'
    CKEDITOR_FILE_UPLOADER = 'be_blog_bp.upload'

    BLOGIN_UPLOAD_PATH = os.path.join(basedir, 'uploads')

    # SQL configure
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DATABASE_USER = os.getenv('DATABASE_USER', 'root')
    DATABASE_PWD = os.getenv('DATABASE_PWD')

    # DEFAULT AVATAR CONFIGURE
    AVATARS_SAVE_PATH = BLOGIN_UPLOAD_PATH + '/avatars/'

    # Mail configure
    BLOGIN_EMAIL_PRE = '[Blogin.] '
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Blogin Admin', MAIL_USERNAME)

    # WHOOSHEE configure
    WHOOSHEE_MIN_STRING_LEN = 1

    # Redis Configure
    # EXPIRE_TIME = 60 * 10

    # Photo Configure
    PHOTO_NEED_RESIZE = 1024 * 1024

    # BAIDU Trans appid
    BAIDU_TRANS_APPID = os.getenv('BAIDU_TRANS_APPID')
    BAIDU_TRANS_KEY = os.getenv('BAIDU_TRANS_KEY')

    # APScheduler config
    SCHEDULER_API_ENABLED = True


class DevelopmentConfig(BaseConfig):
    # 'mysql+pymysql://{}:{}@127.0.0.1/blog?charset=utf8mb4'
    # mysql+pymysql://{}:{}@superliam.mysql.pythonanywhere-services.com/superliam$blog?charset=utf8mb4
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1/blog?charset=utf8mb4'.format(BaseConfig.DATABASE_USER,
                                                                                            BaseConfig.DATABASE_PWD)
    # REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("blogin-test.db")
    WTF_CSRF_ENABLED = False
    import logging

    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.DEBUG)


class ProductionConfig(BaseConfig):
    # mysql+pymysql://{}:{}@localhost/blog?charset=utf8mb4
    # mysql+pymysql://{}:{}@superliam.mysql.pythonanywhere-services.com/superliam$blog?charset=utf8mb4
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1/blog?charset=utf8mb4'.format(BaseConfig.DATABASE_USER,
                                                                                            BaseConfig.DATABASE_PWD)



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
