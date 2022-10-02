
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, jsonify, Flask
from blog.models import Blog, BlogType, LoveMe, LoveInfo, BlogComment, Photo, Notification, VisitStatistics, \
    LikeStatistics, CommentStatistics, Tag, User, FriendLink, Plan
from blog.extension import db
from flask_login import current_user, login_required
from blog.decorators import statistic_traffic
import datetime
from blog.utils import redirect_back
import logging
from logging.handlers import RotatingFileHandler
import blog

blog_bp = Blueprint('blog_bp', __name__)


@blog_bp.route('/', methods=['GET'])
@blog_bp.route('/index/', methods=['GET'])
@statistic_traffic(db, VisitStatistics)
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter_by(delete_flag=1).order_by(Blog.create_time.desc()). \
        paginate(page, per_page=current_app.config['BLOGIN_BLOG_PER_PAGE'])
    blogs = pagination.items
    cates = []
    for blog in blogs:
        cates.append(BlogType.query.filter_by(id=blog.type_id).first().name)
    categories = BlogType.query.all()
    loves = LoveMe.query.first()
    if loves is None:
        loves = 0
    else:
        loves = loves.counts
    plans = Plan.query.filter_by(is_done=0).all()
    su = User.query.filter(User.email == '452458950@qq.com').first()
    flinks = FriendLink.query.filter(FriendLink.flag == 1).all()
    #记录logging
    remote_ip = request.headers.get('X-Real-Ip')
    if remote_ip is None:
        remote_ip = request.remote_addr
    useragent = request.headers.get('User-Agent')
    current_app.logger.info("IP address is: "+remote_ip+"\nDevice and browser: "+useragent)
    return render_template('main/index.html', per_page=current_app.config['BLOGIN_BLOG_PER_PAGE'],
                           pagination=pagination, blogs=blogs, cates=cates, categories=categories,
                           loves=loves, su=su, flinks=flinks, plans=plans)




@blog_bp.route('/blog/article/<blog_id>/')
def blog_article(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    blog.read_times += 1
    replies = []
    cate = BlogType.query.filter_by(id=blog.type_id).first()
    # 顶级评论
    comments = BlogComment.query.filter_by(blog_id=blog_id, parent_id=None).order_by(BlogComment.timestamp.desc()).all()
    # histories = BlogHistory.query.filter_by(blog_id=blog_id).order_by(BlogHistory.timestamps.desc()).all()

    for comment in comments:
        reply = BlogComment.query.filter_by(parent_id=comment.id, delete_flag=0). \
            order_by(BlogComment.timestamp.asc()).all()
        replies.append(reply)
    db.session.commit()
    return render_template('main/blog.html', blog=blog, cate=cate, comments=comments, replies=replies)


@blog_bp.route('/blog/cate/<cate_id>/', methods=['GET', 'POST'])
def blog_cate(cate_id):
    cate = BlogType.query.filter_by(id=cate_id).first()
    categories = BlogType.query.all()
    flinks = FriendLink.query.filter(FriendLink.flag == 1).all()
    plans = Plan.query.filter_by(is_done=0).all()
    return render_template('main/blogCate.html', cate=cate, categories=categories, blogs=cate.blogs, flinks=flinks,
                           plans=plans)




@blog_bp.route('/loveme/')
@statistic_traffic(db, LikeStatistics)
def love_me():
    love = LoveMe.query.first()
    if love is None:
        lv = LoveMe(counts=1)
        db.session.add(lv)
    else:
        love.counts += 1
    # 如果用户已经登录,则记录Username ip,否则记录 匿名用户 IP
    remote_ip = request.headers.get('X-Real-Ip')
    if remote_ip is None:
        remote_ip = request.remote_addr

    if current_user.is_authenticated:
        li = LoveInfo(user=current_user.username, user_ip=remote_ip)
    else:
        li = LoveInfo(user='Anonymous', user_ip=remote_ip)
    db.session.add(li)
    db.session.commit()
    flash('点赞成功!你们的支持就是我前进的动力啦~', 'success')
    return redirect(url_for('.index'))


@blog_bp.route('/blog/comment/', methods=['GET', 'POST'])
@login_required
@statistic_traffic(db, CommentStatistics)
def new_comment():
    comment = request.form.get('comment')
    blog_id = request.form.get('blogID')
    reply_id = request.form.get('replyID')
    parent_id = request.form.get('parentID')
    author = current_user._get_current_object()
    notify = comment
    blog = Blog.query.get_or_404(blog_id)
    comment = BlogComment(body=comment, author=author, blog=blog)
    if reply_id:
        comment.replied = BlogComment.query.get_or_404(reply_id)
        # title = Blog.query.get_or_404(blog_id).title
        new_notify = Notification(target_id=blog_id, send_user=author.username,
                                  receive_id=comment.replied.author_id, msg=notify, target_name=blog.title)
        db.session.add(new_notify)
    if parent_id:
        comment.parent_id = parent_id
    db.session.add(comment)
    db.session.commit()
    current_app.logger.info("New comment: "+ comment.body)
    return redirect(request.referrer)


@blog_bp.route('/blog/comment/delete/', methods=['GET', 'POST'])
@login_required
def delete_comment():
    comm_id = request.form.get('comm_id')
    comment = BlogComment.query.get_or_404(comm_id)
    db.session.delete(comment)
    db.session.commit()
    current_app.logger.info("Delete comment "+comment)
    flash('Comment successfully deleted', 'success')
    return ''


@blog_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if q == '':
        flash('Please input content!', 'info')
        return redirect_back()
    category = request.args.get('category', 'blog')
    if category == 'blog':
        results = Blog.query.whooshee_search(q).paginate(1, 20)
    if category == 'photo':
        results = Photo.query.whooshee_search(q).paginate(1, 20)
    if category == 'tag':
        results = Tag.query.whooshee_search(q).paginate(1, 20)
    results = results.items
    return render_template('main/search.html', results=results, q=q, category=category)
