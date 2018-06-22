# -*- encoding=UTF-8 -*-
# templates文件夹里面的.html文件都是用jinja2模板语法写的；
# 在form.html中加了一点条件判断，把form.html重用为登录失败的模板。
# 最后，一定要把模板放到正确的templates目录下，templates和app.py在同级目录下。

'''
    通过MVC，我们在Python代码中处理M：Model和C：Controller，而V：View是通过模板处理的，这样，我们就成功地把Python代码
和HTML代码最大限度地分离了。model就是更改HTML中的变量；controller就是逻辑代码；view就是HTML的代码以及运行后的页面。
    在Jinja2模板中，我们用{{ name }}表示一个需要替换的变量。很多时候，还需要循环、条件判断等指令语句，在Jinja2中，用
{% ... %}表示指令。
    比如循环输出页码：
{% for i in page_list %}
    <a href="/page/{{ i }}">{{ i }}</a>
{% endfor %}
    如果page_list是一个list：[1, 2, 3, 4, 5]，上面的模板将输出5个超链接。
'''
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def home():
    return render_template('home.html')


@app.route('/signin', methods=['get'])
def signin_from():
    return render_template('form.html')


@app.route('/signin', methods=['post'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)


if __name__ == '__main__':
    app.run(host='127.0.0.3', port=5000, debug=True)
