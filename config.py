import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    #设置密匙要没有规律，别被人轻易猜到哦
    CSRF_ENABLED = True
    SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False