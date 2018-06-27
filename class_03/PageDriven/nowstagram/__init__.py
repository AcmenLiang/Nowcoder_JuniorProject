# -*- encoding=UTF-8 -*-
# 文件功能：做一些初始化；方便外面的模块调用该文件，将该模块包装好的一些moudle暴露出去；这么写类似于模块化编程的感觉。把导出的文件写在这里。
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_pyfile('app.conf')  # 初始化一下，初始化的信息是从这个文件中来的，就是一些配置信息等等
db = SQLAlchemy(app)
from nowstagram import views, models  # 这样工程就打包完了，只要调用__init__就可以找到各个.py文件中的模块


