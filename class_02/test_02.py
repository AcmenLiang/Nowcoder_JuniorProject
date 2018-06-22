# -*- encoding=UTF-8 -*-
# HTTP-Methods 测试，添加get post方法在profile函数中


from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "hello-test HTTP Methods!"


# 传递传参数变量<>   使用方法为输入 http://127.0.0.2:5001/profile/etgj  则将参数变量<etgi>传入尽量并显示
# 在装饰器的参数这里，可以添加methods方法，比如get post delete等等，方式见下方；
@app.route('/profile/<uid>/', methods=['GET', 'post'])
def profile(uid):
    return 'profile: ' + uid


if __name__ == '__main__':
    # 运行，开启debug模式
    app.run(host='127.0.0.2', port=5002, debug=True)
