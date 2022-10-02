
from flask import Blueprint, render_template, send_from_directory, flash, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from blog import basedir, db
from blog.models import Photo, Notification, Tag, VisitStatistics, CommentStatistics
from blog.decorators import statistic_traffic

gallery_bp = Blueprint('gallery_bp', __name__, url_prefix='/gallery')


@gallery_bp.route('/all/', methods=['GET', 'POST'])
@statistic_traffic(db, VisitStatistics)
def index():
    photos = Photo.query.filter_by(level=0).order_by(func.random()).limit(9)
    return render_template('main/gallery.html', photos=photos)


@gallery_bp.route('/photo/<photo_id>', methods=['GET', 'POST'])
def photo(photo_id):
    replies = []
    img = Photo.query.get_or_404(photo_id)
    if img.level == 1:
        flash('未公开的照片，禁止访问!', 'success')
        return redirect(url_for('.index'))
    nex = Photo.query.filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()
    pre = Photo.query.filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()
    if nex is None:
        next_link = None
    else:
        next_link = '/gallery/photo/' + str(nex.id)
    if pre is None:
        pre_link = None
    else:
        pre_link = '/gallery/photo/' + str(pre.id)
    return render_template('main/photo.html', blog=img, nextLink=next_link, preLink=pre_link, replies=replies)


@gallery_bp.route('/<path>/<filename>')
def get_blog_sample_img(path, filename):
    path = basedir + '/uploads/gallery/' + path + '/'
    return send_from_directory(path, filename)


@gallery_bp.route('/tag/<int:tag_id>/')
def tag(tag_id):
    tags = Tag.query.get_or_404(tag_id)
    photos = Photo.query.with_parent(tags).filter_by(level=0).order_by(Photo.create_time.desc())
    return render_template('main/galleryTag.html', photos=photos, tags=tags)
