# -*- encoding=UTF-8 -*-
# 路径映射讲解----flask的URL访问代码



from flask import Flask

app = Flask(__name__)


# 指定一个路径的映射
@app.route('/')
def index():
    return "hello"


# 多映射 ，就是URL已经发布出去了，原有的不能改，但是网址需要增加更多的功能，就在这里增加多映射，不断的在/后增加东西，
# 就可以输入进去并访问。
# 使用方法为输入 http://127.0.0.2:5001/index1  就会显示hello1 达成多映射  就是要在地址后跟上/index即可；
@app.route('/')
@app.route('/index1/')  # 最后记得带上一个/     有结尾自动补齐功能
def index1():
    return "hello1"


# 传递传参数变量<>   使用方法为输入 http://127.0.0.2:5001/profile/etgj  则将参数变量<etgi>传入尽量并显示
@app.route('/profile/<uid>/')
def profile(uid):
    return 'profile: ' + uid


# 转化profile/后接收的数据变量类型 有int str等等； 访问同理
@app.route('/profile/<int:uid>/')
def profile1(uid):
    return 'profile: ' + uid


if __name__ == '__main__':
    # 运行，开启debug模式
    app.run(host='127.0.0.2', port=5001, debug=True)
