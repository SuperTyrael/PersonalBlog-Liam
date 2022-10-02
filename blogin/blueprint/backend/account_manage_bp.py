from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from blogin.models import User, BlogComment
from blogin.extension import db
from flask_login import login_required
from blogin.decorators import permission_required

user_m_bp = Blueprint('user_m_bp', __name__, url_prefix='/backend/interactive')


@user_m_bp.route('/index/')
@login_required
@permission_required
def index():
    page = request.args.get('page')
    pagination = User.query.order_by(User.create_time).paginate(page=page,
                                                                per_page=current_app.config['LOGIN_LOG_PER_PAGE'])
    users = pagination.items
    return render_template('backend/userManager.html', pagination=pagination, users=users)

@user_m_bp.route('/blog-comment/')
@login_required
@permission_required
def blog_comment():
    page = request.args.get('page', default=1, type=int)
    pagination = BlogComment.query.order_by(BlogComment.timestamp).paginate(page=page,
                                                                            per_page=current_app.config[
                                                                                'LOGIN_LOG_PER_PAGE'])
    comments = pagination.items
    return render_template('backend/blog_comments.html', comments=comments, pagination=pagination)


@user_m_bp.route('/lock/blog-comment/<int:com_id>')
@login_required
@permission_required
def unlock_or_lock_blog_comment(com_id):
    blog_com = BlogComment.query.get_or_404(com_id)
    if blog_com is not None and blog_com.delete_flag == 1:
        blog_com.delete_flag = 0
    else:
        blog_com.delete_flag = 1
    db.session.commit()
    flash('Successful!', 'success')
    return redirect(url_for('.blog_comment'))