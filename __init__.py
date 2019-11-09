from flask import Flask
#导入配置文件
from config import Config
#导入数据库相关
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#导入辅助登录模块
from flask_login import LoginManager

from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
#添加配置信息
app.config.from_object(Config)
#创建辅助登录检测模块的对象
login = LoginManager(app)
#用来限制一些只有登录才可以查看的页面@login_required
login.login_view = 'login'

#建立数据库关系
db = SQLAlchemy(app)
#绑定app和数据库，以便进行操作
migrate = Migrate(app,db)

csrf = CSRFProtect(app)

from app import routes,models,forms