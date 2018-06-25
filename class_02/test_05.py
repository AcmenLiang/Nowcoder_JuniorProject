'''
# -*- encoding=UTF-8 -*-
# 重定向 和 error 测试

from flask import Flask, redirect, render_template, request

app = Flask(__name__)


# @app相当于装饰器，即执行route函数，然后在xxx/目录下返回test...这些东西；相当于回调函数，return后的东西给route，在route里面就打印了；
@app.route('/')
def index():
    return 'test-redirect and error'


# 这是重定向之后的新函数，下面的redirect_demo函数，执行后，就定向到这个新函数来执行；定向出一个新路径/newpath，打印的也是test-redirect
@app.route('/newpath')
def newpath():
    return 'test-redirect'


# 这里的/re/<int:code>就是浏览器输入的URL，后面分301和302；即永久转移和临时转移；
# 比如输入xxx/re/302 则会执行newpath函数，在转到xxx/newpath地址；但是下次输入xxx/re/302，还是要重新定向，做HTTP请求等；
# 但是输入xxx/re/301 也会执行newpath函数，在转到xxx/newpath地址；但是下次输入xxx/re/301，浏览器会直接到xxx/newpath，不会再去做HTTP请求了，节约时间。
@app.route('/re/<int:code>')
def redirect_demo(code):
    # return redirect('/newpath')     # 默认为302的重定向方式，不加参数
    return redirect('/newpath', 301)  # 要想是重定向方式为301则应在'/newpath'后加上参数301


# 404error测试，如果输入的页面没找到，则报404错误，则通过装饰器将404传入，会进入not_found.html页面打印出调试信息，方便测试
@app.errorhandler(404)
def page_not_found(error):  # 这里要传入error参数
    return render_template('not_found.html', url=request.url), 404
    # 调用not_found.html的view模板页面，且传入参数url，在HTML页面中打印出来；括号外的404是设置状态为404，方便调试；


if __name__ == '__main__':
    # 运行，开启debug模式
    app.run(host='127.0.0.2', port=5005, debug=True)

'''
