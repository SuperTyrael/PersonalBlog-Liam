
from flask import Blueprint, render_template, send_from_directory, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from imageio import imread
from wtforms import ValidationError

from blogin.decorators import db_exception_handle
from blogin.extension import db
from blogin.forms.auth import ChangePwdForm, EditProfileForm
from blogin.setting import basedir
from blogin.models import User, BlogComment, Notification
from blogin.utils import get_ip_real_add

accounts_bp = Blueprint('accounts_bp', __name__, url_prefix='/accounts')


@accounts_bp.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    page = request.args.get('page', 1, type=int)
    blog_comments = BlogComment.query.filter_by(author_id=user_id, delete_flag=0).order_by(BlogComment.timestamp.desc()).all()
    remote_ip = request.headers.get('X-Real-Ip')
    if remote_ip is None:
        remote_ip = request.remote_addr
    location = get_ip_real_add(remote_ip)
    notifies = Notification.query.filter_by(receive_id=current_user.id, read=0).\
        order_by(Notification.timestamp.desc()).all()
    return render_template('main/accountProfile.html', location = location,               blogComments=blog_comments, notifies=notifies)


@accounts_bp.route('/password/change/', methods=['GET', 'POST'])
@login_required
@db_exception_handle(db)
def change_password():
    form = ChangePwdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.set_password(form.confirm_pwd.data)
        db.session.commit()
        current_app.logger.info("User: "+user.username+"changed password")
        flash('Successfully changed password, please re-login.', 'success')
        return redirect(url_for('auth_bp.logout'))
    return render_template('main/changePassword.html', form=form)


@accounts_bp.route('/profile/edit/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        new_name = form.user_name.data
        user.website = form.website.data
        user.slogan = form.slogan.data
        query_name_user = User.query.filter_by(username=new_name).first()
        if query_name_user is not None and  query_name_user.id != current_user.id:
            flash('Username already exists!', 'danger')
            return render_template('main/editProfile.html', form=form)
        user.username = form.user_name.data
        if form.avatar.data.filename:
            filename = form.avatar.data.filename
            filename = str(current_user.username) + filename
            form.avatar.data.save(basedir + '/uploads/avatars/'+filename)
            img_data = imread(basedir + '/uploads/avatars/'+filename)
            if len(img_data) != len(img_data[0]):
                flash('In order to display the image properly, please upload the image with the same length and width!', 'danger')
                return render_template('main/editProfile.html', form=form)
            user.avatar = '/accounts/avatar/' + filename
        db.session.commit()
        current_app.logger.info("User: "+user.username+"changed the profile")
        flash('Successfully updated profile!', 'success')
        return redirect(url_for('.profile', user_id=current_user.id))
    form.slogan.data = current_user.slogan
    form.website.data = current_user.website
    form.user_name.data = current_user.username
    return render_template('main/editProfile.html', form=form)


@accounts_bp.route('/avatar/<filename>/')
def get_avatar(filename):
    path = basedir + '/uploads/avatars/'
    return send_from_directory(path, filename)


@accounts_bp.route('/mark/<int:notify_id>/')
@login_required
def mark_notify(notify_id):
    no = Notification.query.get_or_404(notify_id)
    no.read = 1
    db.session.commit()
    flash('Success!', 'success')
    return redirect(url_for('.profile', user_id=current_user.id))


@accounts_bp.route('/mark-all/')
@login_required
def mark_all():
    notifies = Notification.query.filter_by(receive_id=current_user.id).all()
    for notify in notifies:
        notify.read = 1
    db.session.commit()
    flash('Success!', 'success')
    return redirect(url_for('.profile', user_id=current_user.id))
