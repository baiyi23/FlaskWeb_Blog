from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField, TextAreaField,SelectField,HiddenField, FileField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo, Length
from flask_wtf.file import FileRequired, FileAllowed
from app.models import User

class LoginForm(FlaskForm):
    #DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名',validators=[DataRequired(message='请输入名户名')])
    password = PasswordField('密码',validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')
    #校验用户名是否重复
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复了，请您重新换一个呗!')
    #校验邮箱是否重复
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱重复了，请您重新换一个呗!')

class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名!')])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')



class PostForm(FlaskForm):
    title = StringField('标题', [DataRequired(), Length(max=255)])
    body = TextAreaField('内容', [DataRequired()])
    #categories = SelectMultipleField('Categories', coerce=int)
    categories=SelectField('文章种类', choices=[],coerce=int )
    body_html = HiddenField()
    submit=SubmitField(render_kw={'value': "提交",'class': 'btn btn-success pull-right'})
    file = FileField(label="文章封面",validators=[FileRequired(),FileAllowed(['png', 'jpg'], '只接收.png和.jpg的图片')])
    #保证数据与数据库同步
    def __init__(self):
        super(PostForm, self).__init__()
        self.categories.choices = [(c.id, c.name) for c in Category.query.order_by('id')]