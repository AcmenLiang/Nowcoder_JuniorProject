# -*- coding:utf8 -*-

from flask import render_template
from flask_mail import Message
from nowstagram import app, mail

# 邮件发送函数
def send_email(to, subject, template, **kwargs):
    # 1.配置 app 对象的邮件服务器地址，端口，用户名和密码等；在app.conf文件中app.config.from_pyfile('app.conf')做了；
    # 2.创建一个 Mail 的实例：mail = Mail(app)；在__init__.py文件中做了；
    # 3.创建一个 Message 消息实例，有三个参数：邮件标题、发送者和接收者
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,  # 邮件的主题
                  sender=app.config['FLASKY_MAIL_SENDER'],  # 邮件是谁发的，也就是我邮箱的地址
                  recipients=[to])  # 邮件是发给谁的，获取调用send_email时候的传入参数即可
    # 4.创建邮件内容，如果是 HTML 格式，则使用 msg.html，如果是纯文本格式，则使用 msg.body
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    '''此处为了全部实现，.txt与.html全部写出来了；由于是显示一个新页面，使用render_template模板；传入的template为文件
    的位置；**kwargs为模板中需要用到的参数，即发给邮件有一个链接，点进去用于激活，产生链接的变量则由kwargs传入；'''
    # 5.调用 mail.send(msg) 发送消息
    mail.send(msg)
