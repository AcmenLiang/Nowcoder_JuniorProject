# -*- encoding=UTF-8 -*-
# log 测试

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler  # RotatingFileHandler这个意思就是过一段时间就会产生一个文件，把内容覆盖掉

app = Flask(__name__)


@app.route('/')
def index():
    return 'test logging'


@app.route('/login/')
def login():
    app.logger.info('log success')  # 每次登录成功则在info.txt中打log，就直接这么调用即可；app.logger.info('...')
    return 'log in ok'


# <level>表示传入参数，传入参数后在函数的()内也要穿入，相当于传入形参；函数内部也就可以使用了；
@app.route('/log/<level>/<msg>/')
def log(level, msg):
    dict = {'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR}  # 定义log的3个级别
    if dict.has_key(level):  # 如果传入了log的level参数，比如error，则通过app.logger.log这个函数，对不同的.txt文件传入log信息msg
        app.logger.log(dict[level], msg)  # 这也是一种调用log的方式，通过传入不同的level给文件打入msg内容
    return 'logged:' + msg  # 这里是在网页页面上显示的


# 设置logger信息函数，设定好了调用一下就可以；打入log的信息还是上面那个函数的使用方法；
def set_logger():
    info_file_handler = RotatingFileHandler('F:\\logs\\info.txt')
    info_file_handler.setLevel(logging.INFO)
    app.logger.addHandler(info_file_handler)

    warn_file_handler = RotatingFileHandler('F:\\logs\\warn.txt')
    warn_file_handler.setLevel(logging.WARN)
    app.logger.addHandler(warn_file_handler)

    error_file_handler = RotatingFileHandler('F:\\logs\\error.txt')
    error_file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_file_handler)


if __name__ == '__main__':
    # 系统启动时，先把log配置好
    set_logger()
    # 运行，开启debug模式
    app.run(host='127.0.0.2', port=5007, debug=True)
