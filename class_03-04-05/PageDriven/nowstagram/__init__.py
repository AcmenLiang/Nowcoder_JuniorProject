# -*- encoding=UTF-8 -*-
# 文件功能：做一些初始化；方便外面的模块调用该文件，将该模块包装好的一些moudle暴露出去；这么写类似于模块化编程的感觉。把导出的文件写在这里。
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # 登录模块
from flask_bootstrap import Bootstrap  # 导航栏优化模块
from flask_mail import Mail  # flask-mail模块，发送邮件

# 用于python链接mysql
import pymysql
pymysql.install_as_MySQLdb()

# 设置flask实例app
app = Flask(__name__)
# break在jinja2模板中是没有的，要添加一个环境变量，自己百度
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
# 初始化一下，初始化的信息是从这个文件中来的，就是一些配置信息等等
app.config.from_pyfile('app.conf')
# 加一个验证，用于flash message功能
app.secret_key = 'nowcoder'
# 声明SQLAlchemy的一个实例，用于建立OMR映射操作数据库
db = SQLAlchemy(app)

# 登录部分初始化
login_manager = LoginManager(app)  # 使用Flask-Login应用最重要的部分是LoginManager类。你应该为你的应用程序创建一个这个类的实例
# login_manager.login_view = '/regloginpage/'  # 指未登录时，访问需要登录的页面，会跳转过去的登录页面。()内参数即跳转页面。
login_manager.login_view = '/wtf/login/'  # 新版登录所需跳转的页面

# 导航栏优化所使用的Bootstrap实例
bootstrap = Bootstrap(app)
# Bootstrap 是 Twitter 开发的一个开源框架，它提供的用户界面组件可用于创建整洁且具有吸引力的网页，而且这些网页还能兼容所有现代 Web 浏览器。

# flask-mail所需实例
mail = Mail(app)

from nowstagram import views, models  # 这样工程就打包完了，只要调用__init__就可以找到各个.py文件中的模块


