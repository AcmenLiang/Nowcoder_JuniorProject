# -*- encoding=UTF-8 -*-
# 文件功能：做一些初始化；方便外面的模块调用该文件，将该模块包装好的一些moudle暴露出去；这么写类似于模块化编程的感觉。把导出的文件写在这里。
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # 登录模块

import pymysql  # 用于python链接mysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')  # break在jinja2模板中是没有的，要添加一个环境变量，自己百度
app.config.from_pyfile('app.conf')  # 初始化一下，初始化的信息是从这个文件中来的，就是一些配置信息等等
app.secret_key = 'nowcoder'  # 加一个验证，用于flash message功能
db = SQLAlchemy(app)  # 声明SQLAlchemy的一个实例，用于简历OMR映射操作数据库
login_manager = LoginManager(app)  # 使用Flask-Login应用最重要的部分是LoginManager类。你应该为你的应用程序创建一个这个类的实例
login_manager.login_view = '/regloginpage/'  # 指未登录时，访问需要登录的页面，会跳转过去的登录页面。()内参数即跳转页面。
from nowstagram import views, models  # 这样工程就打包完了，只要调用__init__就可以找到各个.py文件中的模块


