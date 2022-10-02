
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_
from blogin.forms.forms import ResetPwdForm

from blogin.forms.auth import RegisterForm, LoginForm
from blogin.models import User
from blogin.extension import db
from blogin.utils import get_ip_real_add, generate_token, Operations, validate_token, generate_ver_code

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

#提交数据并发送确认邮件
@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.user_name.data
        pwd = form.confirm_pwd.data
        email = form.user_email.data.lower()
        user = User(username=name, email=email, password=pwd, )
        user.set_password(pwd)
        user.set_role()
        db.session.add(user)
        db.session.commit()
        token = generate_token(user, operation='confirm')
        # send_confirm_email(user=user, token=token)
        flash('Successfully registered', 'success')
        return redirect(url_for('.login'))
    return render_template('main/register.html', form=form)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    # 若当前已有用户登录则返回主页
    if current_user.is_authenticated:
        return redirect(url_for('blog_bp.index'))

    remote_ip = request.headers.get('X-Real-Ip')
    if remote_ip is None:
        remote_ip = request.remote_addr
    form = LoginForm()
    if form.validate_on_submit():
        usr = form.usr_email.data
        pwd = form.password.data
        user = User.query.filter(or_(User.username == usr, User.email == usr.lower())).first()
        if user is not None and user.status == 2:
            flash('您的账号处于封禁状态,禁止登陆！联系管理员解除封禁!', 'danger')
            return redirect(url_for('.login'))

        if user is not None and user.check_password(pwd):
            if login_user(user, form.remember_me.data):
                user.recent_login = datetime.now()
                db.session.commit()
                flash('Successfully logged in, logged location: '+get_ip_real_add(remote_ip), 'success')
                return redirect(url_for('blog_bp.index'))
        elif user is None:
            flash('无效的邮箱或用户名.', 'danger')
        else:
            flash('无效的密码', 'danger')
    return render_template('main/login.html', form=form)


@auth_bp.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('退出成功!', 'success')
    return redirect(url_for('blog_bp.index'))


@auth_bp.route('/forget-password/')
def forget_pwd():
    return render_template('main/auth/forgetPwd.html')



