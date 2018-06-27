# -*- encoding=UTF-8 -*-
# 文件功能：将app中页面的功能写好。视图写在这。

from nowstagram import app, db  # 从application中导入app，不然找不到该模块；从__init__中导入是不行的！！！必须从子目录中导入！！！


@app.route('/')
def index():
    return 'Hello！'
