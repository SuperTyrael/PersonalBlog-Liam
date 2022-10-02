
import datetime
import hashlib
import http
import os

import json
import random
import re
import urllib
from urllib.parse import urlparse, urljoin
import base64

import execjs
import requests
from flask import current_app, request, redirect, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
import jieba
import wordcloud as wc
from PIL import Image, ImageDraw, ImageFont

from blogin.extension import db
from blogin.setting import basedir
from imageio import imread

MONTH = {1: '01-31',
         2: '02-28',
         3: '03-31',
         4: '04-30',
         5: '05-31',
         6: '06-30',
         7: '07-31',
         8: '08-31',
         9: '09-30',
         10: '10-31',
         11: '11-30',
         12: '12-31',
         -1: '11-01',
         0: '12-01'
         }


# def update_contribution():
#     td = datetime.date.today()
#     con = Contribute.query.filter_by(date=td).first()
#     con.contribute_counts += 1


# IP查询工具配置
IP_QUERY = "http://ip-api.com/json/{}?lang=zh-CN&fields=status,message,country,region,regionName,city,lat,lon,query"
IP_REG = '((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))'

# 百度OCR配置
OCR_URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/'
OCR_TOKEN = '24.e45ac0a064909ce3ee8ee1dfb6d48e29.2592000.1606641510.282335-22776145'
OCR_HEADERS = {'content-type': 'application/x-www-form-urlencoded'}
OCR_CATEGORY = {'文字识别': 'accurate_basic', '身份证识别': 'idcard', '银行卡识别': 'bankcard',
                '驾驶证识别': 'driving_license', '车牌识别': 'license_plate'}
BANK_CARD_TYPE = {0: '不能识别', 1: '借记卡', 2: '信用卡'}
LANGUAGE = {'中文': 'zh-CN', '英文': 'en', '日语': 'ja', '法语': 'fr', '俄语': 'ru'}

TRAN_LANGUAGE = {'英译中': 'zh-CN', '中译英': 'en'}
BAIDU_LANGUAGE = {'英译中': 'zh', '中译英': 'en'}

FONT_COLOR = {'红色': (255, 0, 0, 50), '蓝色': (0, 0, 255, 50), '白色': (255, 255, 255, 50), '黑色': (0, 0, 0, 50)}


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


def get_current_time():
    """
    get the current time with yy-mm-dd hh:mm:ss format
    :return: the current time
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_ip_real_add(ip):
    if ip == '127.0.0.1':
        return '本地IP'
    response = requests.get(IP_QUERY.format(ip))
    response = response.text
    response = json.loads(response)
    if response['status'] == 'fail':
        return '定位失败'
    return response['country'] + '-' + response['city']


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        user.confirm = 1
    else:
        user.set_password(new_password)
    db.session.commit()

    return True


def generate_ver_code():
    import random
    return random.randint(134299, 873242)


def split_space(string):
    return str(string).split()


def super_split(string, f):
    return str(string).split(f)


def conv_list(string):
    return list(string)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog_bp.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allow_img_file(filename):
    suffix = filename.split('.')[0]
    if suffix not in ['jpg', 'png', 'jpeg']:
        return False
    return True


def allow_txt_file(filename):
    suffix = filename.split('.')[0]
    if suffix != 'txt':
        return False
    return True


class ImageAddMarkBase:
    def __init__(self, image, text, font_size, save_path, font_color):
        self.image = image
        self.text = text
        self.font_size = font_size
        self.save_path = save_path
        self.font_color = font_color
        self.font = None
        self.font_len = None
        self.image_draw = None
        self.rgba_image = None
        self.text_overlay = None

    def generate_base(self):
        self.font = ImageFont.truetype(basedir + '/res/STFangsong.ttf', self.font_size)
        # 添加背景
        new_img = Image.new('RGBA', (self.image.size[0] * 3, self.image.size[1] * 3), (0, 0, 0, 0))
        new_img.paste(self.image, self.image.size)

        # 添加水印
        self.font_len = len(self.text)
        self.rgba_image = new_img.convert('RGBA')
        self.text_overlay = Image.new('RGBA', self.rgba_image.size, (255, 255, 255, 0))
        self.image_draw = ImageDraw.Draw(self.text_overlay)


def resize_img(path, w_zoom, h_zoom):
    """
    生成缩略图
    :param h_zoom: 高放大比例
    :param w_zoom: 宽放大比例
    :param path: 文件路径
    :return: 返回缩略图，缩小尺寸到原来的三分之一
    """
    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    img = img.resize((int(width * w_zoom), int(height * h_zoom)), Image.ANTIALIAS)
    return img

import hashlib

def get_md5(s):
    m = hashlib.md5()
    if isinstance(s, str):
        m.update(s.encode('utf-8'))
    return m.hexdigest()

