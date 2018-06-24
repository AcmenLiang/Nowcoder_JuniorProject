# -*- encoding=UTF-8 -*-
# 静态和模板文件测试


from flask import Flask, render_template

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'  # 开头，行语法表达(line statements),可见HTML文件中的# for color in colors:


@app.route('/')
def index():
    return "hello-test!"


# 传递传参数变量<>   使用方法为输入 http://127.0.0.2:5001/profile/etgj  则将参数变量<etgi>传入尽量并显示
# 在装饰器的参数这里，可以添加methods方法，比如get post delete等等，方式见下方；
# return后面的内容通过模板来输出，即大部分内容已经写完了，但是需要把参数填进来，这就是模板；
# 通过使用render_template来调用，比如下面的return语句

# 达到前后端分离的目的，python只改model和controller部分，HTML只需要负责页面即可
@app.route('/profile/<uid>/', methods=['GET', 'post'])
def profile(uid):
    colors = ('red', 'green')  # 传入一个元祖变量，元祖是各个元素不可改变
    infos = {'nowcoder': 'abc', 'google': 'def'}
    return render_template('profile.html', uid=uid, colors=colors, infos=infos)  # 多传入一个变量colors，用于模板中的遍历
    # 调用模板，用.html文件写的，只需要传入变量，模板中的{{uid}}会跟随传入的变量而改变


if __name__ == '__main__':
    # 运行，开启debug模式
    app.run(host='127.0.0.2', port=5003, debug=True)
