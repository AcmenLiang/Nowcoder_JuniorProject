# -*- encoding=UTF-8 -*-
# request and response 测试


from flask import Flask, render_template, request, make_response

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'  # 开头，行语法表达(line statements),可见HTML文件中的# for color in colors:


@app.route('/')
def index():
    return "hello-test requests!"


# 测试request response基本功能
@app.route('/request')
def request_demo():
    key = request.args.get('key', 'defaultkey') + '<br>'
    res = request.args.get('key', 'defaultkey') + '<br>'
    res = res + request.url + '++' + request.path + '<br>'  # 通过request获得URL和path
    for property in dir(request):
        res = res + str(property) + '|==|<br>' + str(eval('request.' + property)) + '<br>'

    response = make_response(res)  # 请求来了做出返回
    response.set_cookie('nowcoderid', key)  # 设定cookie，服务器给客户端一个响应，设定的cookie得到显示；response控制cookie
    response.status = '404'  # response设定状态
    response.headers['nowcoder'] = 'hello~~'  # 把返回的东西放在的response header部分，可以直接看到
    return response


if __name__ == '__main__':
    # 运行，开启debug模式
    app.run(host='127.0.0.2', port=5004, debug=True)
