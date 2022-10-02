
import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_share import Share
from flask_avatars import Avatars
from flask_whooshee import Whooshee

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
ckeditor = CKEditor()
login_manager = LoginManager()
share = Share()
avatar = Avatars()
whooshee = Whooshee()


@login_manager.user_loader
def load_user(user_id):
    from blogin.models import User
    user = User.query.filter_by(id=user_id).first()
    return user


login_manager.login_view = 'auth_bp.login'
login_manager.login_message = u'请先登陆!'
login_manager.login_message_category = 'danger'



