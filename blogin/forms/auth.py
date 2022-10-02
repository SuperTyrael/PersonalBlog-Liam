
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, BooleanField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from blogin.models import User

# noinspection PyMethodMayBeStatic


class LoginForm(FlaskForm):
    usr_email = StringField(u'email/username', validators=[DataRequired(message='email and username cannot be empty')],
                            render_kw={'placeholder': 'Please input email or username'})
    password = StringField(u'Password',
                           validators=[DataRequired(message='Password cannot be empty'),
                                       Length(min=8, max=40, message='Password should in between 8 to 40 digits')],
                           render_kw={'type': 'password','placeholder': 'Please input password'})
    remember_me = BooleanField('Remember me')
    submit = SubmitField(u'Login', render_kw={'class': 'btn btn-secondary'})


class RegisterForm(FlaskForm):
    user_name = StringField(u'Username',
                            validators=[DataRequired(message='Username cannot be empty'),
                                        Length(min=1, max=16, message='Username长度限定在1-16位之间'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='Username can only contain numbers, letters and underscores.')],
                            render_kw={'placeholder': 'Please input username in between 1 to 8 words'})
    user_email = StringField(u'Email',
                             validators=[DataRequired(message='Email cannot be empty'),
                                         Length(min=4, message='Email must longer than 4 digits')],
                             render_kw={'placeholder': '请输入Email', 'type': 'email'})
    password = StringField(u'Password',
                           validators=[DataRequired(message='Password cannot be empty'),
                                       Length(min=8, max=40, message='User password length limited to 8-40 digits'),
                                       EqualTo('confirm_pwd', message='Two inconsistent passwords')],
                           render_kw={'placeholder': 'Please input password', 'type': 'password'})
    confirm_pwd = StringField(u'Confirm password',
                              validators=[DataRequired(message='Password cannot be empty'),
                                          Length(min=8, max=40, message='User password length limited to 8-40 digits')],
                              render_kw={'placeholder': 'Please confirm passwords', 'type': 'password'})
    submit = SubmitField(u'Create', render_kw={'class': 'btn btn-secondary'})

    def validate_user_name(self, filed):
        if User.query.filter_by(username=filed.data).first():
            raise ValidationError('Username already be registered.')

    def validate_user_email(self, filed):
        if User.query.filter_by(email=filed.data.lower()).first():
            raise ValidationError('Email already be registered.')


class ChangePwdForm(FlaskForm):
    origin_pwd = StringField(u'原始密码', validators=[DataRequired(message='原始密码不能为空.')],
                             render_kw={'placeholder': '请输入原始密码', 'type': 'password'})
    change_pwd = StringField(u'新的密码', validators=[DataRequired(message='修改后的密码不能为空.'),
                                                  EqualTo('confirm_pwd', message='两次输入密码不一致.')],
                             render_kw={'placeholder': '请输入新的密码', 'type': 'password'})
    confirm_pwd = StringField(u'确认密码', validators=[DataRequired(message='原始密码不能为空')],
                              render_kw={'placeholder': '请再次确认密码', 'type': 'password'})
    submit = SubmitField(u'修改', render_kw={'class': 'btn btn-secondary'})

    def validate_origin_pwd(self, filed):
        if not User.query.filter_by(username=current_user.username).first().check_password(filed.data):
            raise ValidationError('原始密码错误')


class EditProfileForm(FlaskForm):
    user_name = StringField(u'Username',
                            validators=[DataRequired(message='Username cannot be empty'),
                                        Length(min=1, max=16, message='Username长度限定在1-16位之间'),
                                        Regexp('^[a-zA-Z0-9_]*$',
                                               message='Username can only contain numbers, letters and underscores.')],
                            render_kw={'placeholder': '请输入Username长度1-8之间'})
    website = StringField(u'个人网站', render_kw={'placeholder': '请输入个人网站', 'type': 'url'})
    avatar = FileField(u'个人头像', validators=[FileAllowed(['png', 'jpg'], '只接收png和jpg图片')])
    slogan = TextAreaField(u'个性签名', render_kw={'placeholder': '签名不超过200个字符'})
    submit = SubmitField(u'保存', render_kw={'class': 'btn btn-secondary'})