# -*- encoding=UTF-8 -*-
# 文件功能：将app中页面的功能写好。视图写在这。

from nowstagram import app, db  # 从application中导入app，不然找不到该模块；从__init__中导入是不行的！！！必须从子目录中导入！！！
from models import User, Image, Comment  # 由于view与model文件在泳衣目录，故直接这么导入即可，将这3个类导入；
from flask import render_template, redirect, request, flash, get_flashed_messages
# render_templatejinja2中的模板；redirect重定向；request用于get post中的请求；get_flashed_messages用于消息闪现
from flask_login import login_user, logout_user, login_required, current_user  # 这4部分即登陆登出所需的函数
import hashlib  # md5加密用
import random  # 产生随机数
import json


# python的装饰器，传入一个/就可以直接下面的函数，注意URL不是localhost/index，index只是个函数；这里就是127.0.0.1:5001/
@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    # 查询Image类(表)中的图，查出10张来，按图片id的降序排列取出给images变量；
    # images用于在render_template中传入参数，这就是jinja2模板语言了，传入的参数在html文件中继续应用，用于显示；
    return render_template('index.html', images=images)
    # render_template是jinja2模板的用法(在class_02讲过)，即MVC的开发模式，调用HTML写好的页面做显示；直接显示.html中页面
    # 的样子，其中里面还加入了CSS的渲染等，这个就是前端做的任务了；


# 图片详情页的开发；URL为127.0.0.1:5001/image/图片id ；<int:image_id> 对route传入参数，相当于传入形参，以前讲过；
@app.route('/image/<int:image_id>/')
def image(image_id):
    image = Image.query.get(image_id)  # 用的单数，就一张图片，获取到了图片的变量
    if image == None:
        return redirect('/')  # 重定向的页面跳转，在class_02讲过；如果图片为空，则重定向回首页；
    comments = Comment.query.filter_by(image_id=image_id).order_by(db.desc(Comment.id)).limit(20).all()
    return render_template('pageDetail.html', image=image, comments=comments)  # 否则就进入图片详情页；传入.html网页作为模板


# 个人详情页的开发；意思都和上面差不多，就不多写了
@app.route('/profile/<int:user_id>/')
@login_required  # 给profile首页加上权限，即不登录的话无法访问该页内容，此处的装饰器是flask-login中的东西
# 即假如没有登录的话，点击看其他人的个人详情页，图片详情页都没法看
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    # 现在就不是全部读取了，只读取了第一页，且第一页有3张图；即现在初始化的时候只显示3张图，原先是一下10张全读进去。
    # 所以为了显示全部的图，要点击更多按钮，进行刷新，刷新我们就要用AJAX异步刷新的方法。所以请看下面的def user_images方法。
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3,
                                                               error_out=False)  # 注：paginate是分页查询的一个关键字，原先讲过。
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)  # 第一次显示也要判断下是否还有下一页，不然没有的话就不显示更多按钮了


#   实现AJAX的关键函数，个人详情页实现AJAX需要这个图片查询函数做辅助。
# 新加一个请求，这个请求可以把页面分页的显示用户的图片
# 每次点击更多之后，都会查询到新的一页图片，将该页图片的数据存入一个map中，返回给前端，让他们显示
#   效果演示：本地调试时比如输入 http://127.0.0.1:5001/profile/images/50/2/3/
# 则返回如下样式字符串：{"has_next": true, "images": [{"url": "http://images.nowcoder.com/head/99m.png", "comment_count": 3, "id": 494}, {"url": "http://images.nowcoder.com/head/840m.png", "comment_count": 3, "id": 495}, {"url": "http://images.nowcoder.com/head/61m.png", "comment_count": 3, "id": 496}]}
# 剩下的就将该接口返回给前端显示即可。
@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    # 1.查询用户的数据
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    # 2.将查询到的数据进行返回，不断获取新的翻页数据后，总有读完的时候，即没法点击更多了，前端是需要后端通知的。
    # 选择用一个map返回数据。
    # 3.设立是否还有下一页的标志
    map = {'has_next': paginate.has_next}  # has_next是paginate中的一个属性，直接调用即可
    images = []
    # 4.每页的图片信息存入map中，最终返回json格式
    for image in paginate.items:
        imgvo = {'id': image.id, 'url': image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)


# flash message用的比较多，独立成一个函数；category为分类闪现的应用，具体可看下面资料：
# http://docs.jinkan.org/docs/flask/patterns/flashing.html
def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)  # 将flash消息存入session中，待后面用的时候提取出来
    return redirect(target)  # 重定向回目标页


# 注册登录页的开发；用flask的装饰器，写URL的入口地址，用flask中jinja2模板，进入后利用login.html来view出来，MVC模式
@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    # 对每次返回到注册登录页的flash message进行一个提取，然后传入前端令其显示出来；这里用到了过滤闪现和分类闪现；
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html', msg=msg,
                           next=request.values.get('next'))  # 传入next为了用户体验优化，可以跳回注册前点击的页面，而不是直接返回首页


# 注册函数的开发；即点击注册按钮后后台处理的过程；
# 1.获取用户提交的用户名/密码；2.业务处理，对用户名/密码进行业务逻辑判断；3.密码进行salt加密；4.将数据插入数据库；
# 5.注册好后自动登录；6.最终返回登录注册页，要在登录注册页做一个消息的提取，显示注册状态等。
@app.route('/reg/', methods={'post', 'get '})
def reg():
    # 1.获取用户提交的用户名/密码；
    # request.args.get('xx')   获取get,post请求中URL里的xx参数
    # request.form.get('xx')   获取post请求中body里的xx参数
    # request.values.get('xx') 获取get，post请求中URL，body里的xx参数(即获得所有参数，推荐用这种)
    username = request.values.get('username').strip()  # 获取username参数，用values来获取；strip是去除带来的一些空格等
    password = request.values.get('password').strip()  # 这两句为注册后获取的用户提交的用户名/密码的注册信息

    # 2.业务逻辑处理，看是否出测过该username，username/password是否存在等等异常判断
    user = User.query.filter_by(username=username).first()  # 对获取到的username进行过滤寻找，看是否存在重名的username
    if user != None:
        return redirect_with_msg('/regloginpage', u'用户名已经存在', 'reglogin')
    # 判断是否为空的用户名与密码；后面可以自己加更多可能的业务判断
    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', u'用户名或密码不能为空', 'reglogin')

    # 3.密码进行salt加密，即对md5的加密方式进行提高加密等级，增加一个字符串再进行MD5加密；
    salt = '.'.join(random.sample('012345679sadfasfvimAVHJWESRIBPFAQ', 10))
    m = hashlib.md5()  # 生成md5密码
    m.update(password + salt)
    password = m.hexdigest()  # 加上salt后生成新密码，在数据库中可以看到，是一串字符，加密过的，用的时候会解析，防止被破解，这就是md5加密

    # 4.将新数据提交给数据库，最后要commit一下
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    # 5.注册好了之后自动登录
    login_user(user)  # 登录用户，user为刚才注册好的，使用flask-login中的库函数

    # 用户体验优化，即注册/登录完后可以跳回注册前点击的页面，而不是直接返回首页；这里用一个next变量即可实现
    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)

    # 6.最终将返回首页，重定向回首页
    return redirect('/')


# 登录函数的开发;即点击登录按钮后后台处理的过程；
# 1.获取用户名/密码；2.业务逻辑判断用户名/密码；3.最终则登录用户并回首页；
@app.route('/login/', methods={'get', 'post'})
def login():
    # 1.获取用户名/密码
    username = request.values.get('username').strip()  # 获取登录时提交的用户名/密码
    password = request.values.get('password').strip()
    user = User.query.filter_by(username=username).first()  # 查询username是否存在，存在则为非None，不存在则为None
    # 2.业务逻辑判断用户名
    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', u'用户名或密码不能为空', 'reglogin')
    if user == None:  # 进入if则代表没有该用户名
        return redirect_with_msg('/regloginpage', u'用户名不存在', 'reglogin')
    # 3.业务逻辑判断密码----这里用到了将提取到的密码进行md5加密然后与数据库中的密码进行比对的方法
    m = hashlib.md5()
    m.update(password + user.salt)
    if m.hexdigest() != user.password:
        return redirect_with_msg('/regloginpage', u'密码错误', 'reglogin')
    login_user(user)  # 最终则登录用户

    # 用户体验优化，即注册/登录完后可以跳回注册前点击的页面，而不是直接返回首页；这里用一个next变量即可实现
    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)

    # 4.登陆后重定向会首页
    return redirect('/')


# 登出用户函数的开发：用于点击登出之后的跳转页，跳转过来就进行token,session的删除等
@app.route('/logout/')
def logout():
    logout_user()  # flask-login库中的函数，删除token，session等
    return redirect('/')  # 当登出之后自动重定向到首页
