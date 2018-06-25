'''
# -*- encoding=UTF-8 -*-
# flash message 测试

from flask import Flask, flash, get_flashed_messages, redirect

app = Flask(__name__)
app.secret_key = 'nowcoder'  # 两个页面互相跳转需要一个session的ID,如果不加则flash message无法使用；正常情况下这里的UUID应该设置一个无序随机值


@app.route('/')
@app.route('/index/')
def index():
    res = ''
    # 存入flash的消息即在get_flashed_messages中，for loop遍历存入res，然后打印即可看到效果
    for msg, category in get_flashed_messages(with_categories=True):
        res = res + category + msg + '<br>'
    res += 'hello'
    return 'test-flash message' + res


# 进入login页面后，有一条语句flash('登陆成功')，即将“登录成功”压入了消息队列中了；然后再重定向回主页
# 如果直接返回ok，还是会把登陆成功压入flash，在后面的调用中一样会一起打印出来
@app.route('/login')
def login():
    # flash('登陆成功')  # 未加category的情况
    flash('登陆成功', 'info')  # flash的message除了传一些文本之外，还可以加一些category(即第二个参数)，用处就是有时候会加一些过滤之类的
    # return 'ok'
    return redirect('/')


if __name__ == '__main__':
    # 运行，开启debug模式
    app.run(host='127.0.0.2', port=5006, debug=True)
'''
