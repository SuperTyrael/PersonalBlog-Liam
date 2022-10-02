
import os
from datetime import datetime
# from bs4 import BeautifulSoup
from flask import Blueprint, render_template, send_from_directory, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required

from blogin.blueprint.backend.forms import AddFlinkForm, AddPlanForm
from blogin import basedir
from blogin.decorators import permission_required
from blogin.models import FriendLink, States, Plan
from blogin.extension import db
import psutil

other_bp = Blueprint('other_bp', '__name__', url_prefix='/backend')

@other_bp.route('/logs/')
@login_required
@permission_required
def look_logs():
    logs = []
    app_log_path = basedir + '/logs/'
    nginx_log_path = '/var/log/nginx/'
    # 运行日志
    get_log_file_info(app_log_path, logs)
    get_log_file_info(nginx_log_path, logs, log_cate='nginx access/error 文件日志!')
    return render_template('backend/logs.html', logs=logs)


def get_log_file_info(app_log_path, logs, log_cate='程序运行日志！'):
    for app_log in get_log_files(app_log_path):
        app_log_update_time = get_file_mtime(app_log)
        app_log_size = os.path.getsize(app_log)
        logs.append([os.path.split(app_log)[1], log_cate, app_log_update_time, app_log, str(app_log_size) + 'byte'])


@other_bp.route('/logs/detail/<path:file_path>/')
@login_required
@permission_required
def log_detail(file_path):
    """
    显示日志文件内容
    :param file_path: 日志文件路径
    :return: 日志文件详细内容页面
    """
    contents = []
    with open('/' + file_path) as f:
        for line in f.readlines():
            line.strip('\n')
            if line.__contains__('[GET]') or line.__contains__('[POST]'):
                line = "<span style='color: red;'>" + line + "</span>"
            if line.__contains__('Traceback'):
                line = "<span style='color: red;'>" + line + "</span>"
            contents.append(line)
    return render_template('backend/logDetail.html', contents=contents, path='/' + file_path)


@other_bp.route('/logs/download/')
@login_required
@permission_required
def download_log_file():
    """
    下载备份日志文件
    :return: 日志文件
    """
    file = request.args.get('filename')
    return send_from_directory(os.path.split(file)[0], filename=os.path.split(file)[1], as_attachment=True)


def get_file_mtime(path):
    """
    获取文件最后修改时间
    :param path: 文件路径
    :return: 文件最后修改时间
    """
    timestamp = os.path.getmtime(path)
    timestamp = datetime.fromtimestamp(timestamp)
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp


def get_log_files(path):
    """
    便利文件夹，获取文件夹中的log文件路径
    :param path: 需要遍历的目标文件夹
    :return: 目标文件夹根目录下的所有log文件
    """
    fl_ls = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.__contains__('log') and not f.__contains__('.gz'):
                fl_ls.append(os.path.join(root, f))
    return fl_ls


@other_bp.route('/flink/add/', methods=['GET', 'POST'])
@login_required
@permission_required
def add_flink():
    form = AddFlinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.link.data
        desc = form.desc.data
        status = States.query.filter(States.name=='正常').first()
        flink = FriendLink(name=name, link=url, flag=status.id, desc=desc)
        db.session.add(flink)
        db.session.commit()
        return redirect(url_for('blog_bp.index'))
    return render_template('backend/addFlink.html', form=form)


@other_bp.route('/flink/edit/', methods=['GET', 'POST'])
@login_required
@permission_required
def edit_flink():
    flinks = FriendLink.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        desc = request.form.get('desc')
        flink_id = request.form.get('btnID')
        flink = FriendLink.query.get_or_404(flink_id)
        if flink:
            flink.name = name
            flink.link = url
            flink.desc = desc
            db.session.commit()
        return jsonify({'tag': 1})
    return render_template('backend/editFlink.html', flinks=flinks)


@other_bp.route('/flink/lock-or-unlock/<int:flink_id>/', methods=['GET'])
@login_required
@permission_required
def lock_or_unlock_flink(flink_id):
    fl = FriendLink.query.get_or_404(flink_id)
    if fl.flag == 1:
        fl.flag = 2
    else:
        fl.flag = 1
    db.session.commit()
    flash('Successful!', 'success')
    return redirect(url_for('.edit_flink'))


@other_bp.route('/plan/add/', methods=['GET', 'POST'])
@login_required
@permission_required
def add_plan():
    form = AddPlanForm()
    if form.validate_on_submit():
        plans = Plan.query.filter_by(is_done=0).all()
        if len(plans) >= 3:
            flash('你已经有三条计划了,不要好高骛远哦!', 'info')
            return redirect(url_for('blog_bp.index'))
        plan = Plan.query.filter_by(title=form.title.data).first()
        if plan:
            flash('该计划已经存在', 'info')
            return render_template('backend/addPlan.html', form=form)

        plan = Plan(title=form.title.data, total=form.total.data, timestamps=form.timestamps.data)
        db.session.add(plan)
        db.session.commit()
        flash('添加计划成功', 'success')
        return redirect(url_for('.add_plan'))
    return render_template('backend/addPlan.html', form=form)


@other_bp.route('/plan/edit/', methods=['GET', 'POST'])
@login_required
@permission_required
def edit_plan():
    plans = Plan.query.all()
    return render_template('backend/editPlan.html', plans=plans)
