
from datetime import datetime

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SelectField, TextAreaField, FileField, SubmitField, DateTimeField, DateField
from wtforms.validators import Length, DataRequired, ValidationError
from blogin.models import BlogType, FriendLink


class PostForm(FlaskForm):
    title = StringField(u'Blog title', validators=[Length(min=3, max=50, message='Length of username should between 3 to 20 digits')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': 'Input your post title'})
    blog_type = SelectField(label=u'Blog category',
                            default=0,
                            coerce=int)
    blog_level = SelectField(label=u'Blog permission', choices=[(1, 'Public'), (2, 'Private')], validators=[DataRequired()],
                             default=1, coerce=int)
    brief_content = TextAreaField(u'Blog introduction', validators=[DataRequired()])
    blog_img_file = FileField(label=u'博客示例图',
                              validators=[DataRequired(), FileAllowed(['png', 'jpg'], 'Only .png or .jpg formate pic')],
                              render_kw={'value': "Upload", 'class': 'btn btn-default'})
    body = CKEditorField('Body', validators=[DataRequired(message='Please input content of post')])
    submit = SubmitField(u'Publish')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        categories = BlogType.query.all()
        self.blog_type.choices = [(cate.id, cate.name) for cate in categories]


class EditPostForm(FlaskForm):
    title = StringField(u'Blog title', validators=[Length(min=3, max=50, message='Length of username should between 3 to 20 digits')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': 'Input your post title'})
    blog_type = SelectField(label=u'Blog category', default=0, coerce=int)
    blog_level = SelectField(label=u'Blog permission', choices=[(1, '公开'), (2, '私有')], validators=[DataRequired()],
                             default=1, coerce=int)
    brief_content = TextAreaField(u'Blog introduction', validators=[DataRequired()])
    blog_img_file = FileField(u'博客示例图', validators=[FileAllowed(['png', 'jpg'], 'Only .png or .jpg formate pic')],
                              render_kw={'value': "Upload", 'class': 'btn btn-default'})
    body = CKEditorField('Body', validators=[DataRequired(message='Please input content of post')])
    submit = SubmitField(u'Save')

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        categories = BlogType.query.all()
        self.blog_type.choices = [(cate.id, cate.name) for cate in categories]


class AddPhotoForm(FlaskForm):
    # 添加相册照片前端表单
    photo_title = StringField(u'lPhoto title',
                              validators=[DataRequired(), Length(min=1, max=20, message='Length of  title should between 1 to 20 digits')],
                              render_kw={'class': '', 'rows': 50, 'placeholder': 'Input title of photo'})
    photo_desc = TextAreaField(u'Photo description',
                               validators=[DataRequired(), Length(min=3, max=250, message='Length of photo description should between 3 to 250 words')])
    img_file = FileField(label=u'相片文件',
                         validators=[DataRequired(), FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                         render_kw={'value': "Upload", 'class': 'btn btn-default'})
    photo_level = SelectField(label=u'Photo permission', choices=[(1, 'Public'), (2, 'Private')], validators=[DataRequired()],
                              default=1, coerce=int)
    tags = StringField(u'Tag of Photo',
                       validators=[DataRequired(), Length(min=1, max=50, message='Length of tag should between 1 to 50 words')],
                       render_kw={'placeholder': 'Please input tag of photo'})
    submit = SubmitField(u'Publish')


class EditPhotoInfoForm(FlaskForm):
    photo_title = StringField(u'Photo title',
                              validators=[DataRequired(), Length(min=1, max=20, message='Length of  title should between 1 to 20 digits')],
                              render_kw={'class': '', 'rows': 50, 'placeholder': 'Input title of photo'})
    photo_desc = TextAreaField(u'Photo description',
                               validators=[DataRequired(), Length(min=3, max=250, message='Length of photo description should between 3 to 250 words')])
    submit = SubmitField(u'Save')


class AddFlinkForm(FlaskForm):

    name = StringField(u'FriendLink name', validators=[DataRequired(), Length(min=3, max=50, message='Length of username should between 3 to 20 digits')],
                       render_kw={'class': '', 'rows': 50, 'placeholder': 'Please input friendlink name'})
    link = StringField(u'URL path', validators=[DataRequired(), Length(min=3, max=50, message='Length of username should between 3 to 20 digits')],
                       render_kw={'class': '', 'rows': 50, 'placeholder': 'Please input URL of friendlink'})
    desc = StringField(u'FriendLink description', validators=[Length(min=3, max=50, message='Length of username should between 3 to 20 digits')],
                       render_kw={'class': '', 'rows': 50, 'placeholder': 'Please input description of friendlink'})
    submit = SubmitField(u'Add friendlink')

    def validate_name(self, filed):
        if FriendLink.query.filter_by(name=filed.data).first():
            raise ValidationError('Name already exist!')

    def validate_link(self, filed):
        if FriendLink.query.filter_by(link=filed.data.lower()).first():
            raise ValidationError('URL already added!')


class AddPlanForm(FlaskForm):
    title = StringField(u'nPlan name', validators=[DataRequired(),
                                                Length(min=2, max=20, message='Length of plan name should between 1 to 30 words')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': 'Please input the name of plan'}
                        )
    total = StringField(u'Total progress', validators=[DataRequired()],
                        render_kw={'class': '', 'rows': 50, 'type': 'number', 'placeholder': 'Please input the total progress'}
                        )
    timestamps = DateField(u'Start at', default=datetime.today())
    submit = SubmitField(u'Add plan')
