from app import app,db
from flask import render_template,flash,redirect,url_for,request
from app.forms import LoginForm,RegistrationForm,EditProfileForm
from flask_login import current_user, login_user,logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

from app import csrf

@app.route('/')
@app.route('/index')
@login_required

def index():

    posts = [
        {
            'author':{'username':'刘'},
            'body':'这是模板模块中的循环例子～1'

        },
        {
            'author': {'username': '忠强'},
            'body': '这是模板模块中的循环例子～2'
        }
    ]
    return render_template('index.html',title='我的',posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    #判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))


    form=LoginForm()
    #验证表格中的数据格式是否正确
    if form.validate_on_submit():
        #根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        #闪现的信息会出现在页面，当然在页面上要设置
        flash('用户登录的名户名是:{} , 是否记住我:{}'.format(
            form.username.data,form.remember_me.data))
        if user is None or not user.check_password(form.password.data):
            #如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')
            #然后重定向到登录页面
            return redirect(url_for('login'))
        #这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user,remember=form.remember_me.data)

        #此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        #如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        #综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return redirect(url_for('index'))
    return render_template('login.html',title='登录',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user,'body':'测试Post #1号'},
        {'author':user,'body':'测试Post #2号'}
    ]

    return render_template('user.html',user=user,posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的提交已变更.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑',
                           form=form)


@app.route('/post', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def post():
    title="写文章"
    form = PostForm()
    if form.validate_on_submit():
        #basepath = os.path.dirname(__file__)  # 当前文件所在路径
        #fileGet='uploads/assignment{}'.format(HOMEWORK_TIME)
        #upload_path = os.path.join(basepath,fileGet,secure_filename(fpy.filename))
        savepic_path = 'app/static/assets/img/'+form.file.data.filename
        form.file.data.save(savepic_path)  #处理封面地址
        cate=Category.query.filter_by(name=dict(form.categories.choices).get(form.categories.data)).first_or_404()  #处理类别
        cate.number=cate.number+1
        article=Article(title=form.title.data,body = form.body.data,create_time = datetime.now(),pic_path='static/assets/img/'+form.file.data.filename,category_id=cate.id)  #新建文章
        db.session.add(article)
        db.session.commit()
        flash('上传成功！')
        return redirect(url_for('index'))
    #if request.method=='POST':
    #   fpic=request.files['editormd-image-file']
    #   bodypic_path='app/static/pic/'+fpic.filename
    #   fpic.save(bodypic_path)
    return render_template('post.html',title=title, form=form,category=category)

