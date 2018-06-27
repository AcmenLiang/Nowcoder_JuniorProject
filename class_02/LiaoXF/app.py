# -*- encoding=UTF-8 -*-
'''
 写一个app.py，处理3个URL，分别是：
    GET /：首页，返回Home；
    GET /signin：登录页，显示登录表单；
    POST /signin：处理登录表单，显示登录结果。
    注意噢，同一个URL/signin分别有GET和POST两种请求，映射到两个处理函数中。
Flask通过Python的装饰器在内部自动地把URL和函数给关联起来，所以，我们写出来的代码就像这样：
'''

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'


# 使用方法为输入 http://127.0.0.1:5000/signin 不多说
@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''


@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    # 实际的Web App应该拿到用户名和口令后，去数据库查询再比对，来判断用户是否能登录成功。
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'


if __name__ == '__main__':
    # 自己设定URL地址以及端口号，只要不跟当前其他程序用的冲突即可；
    app.run(host='127.0.0.1', port=5000, debug=True)
