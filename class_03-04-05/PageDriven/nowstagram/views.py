# -*- encoding=UTF-8 -*-
# 文件功能：将app中页面的功能写好。视图写在这。

from nowstagram import app, db  # 从application中导入app，不然找不到该模块；从__init__中导入是不行的！！！必须从子目录中导入！！！
from models import User, Image, Comment  # 由于view与model文件在泳衣目录，故直接这么导入即可，将这3个类导入；
from flask import render_template, redirect, request, flash, get_flashed_messages, send_from_directory, url_for
# render_templatejinja2中的模板；redirect重定向；request用于get post中的请求；get_flashed_messages用于消息闪现;
# send_from_directory是flask中直接显示某个本地文件中图片用的库函数；
from flask_login import login_user, logout_user, login_required, current_user  # 这4部分即登陆登出所需的函数
from nowstagram.email import send_email
import hashlib  # md5加密用
import random  # 产生随机数
import uuid  # 产生唯一识别码，用于给文件名更名
import os
import json
from qiniusdk import qiniu_upload_file  #七牛


from nowstagram.reglogin.forms import LoginForm, RegisterForm



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            三大详情页开发以及AJAX异步刷新
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# python的装饰器，传入一个/就可以直接下面的函数，注意URL不是localhost/index，index只是个函数；这里就是127.0.0.1:5001/
@app.route('/')
def index():
    # images = Image.query.order_by('id desc').limit(10).all()
    # 查询Image类(表)中的图，查出10张来，按图片id的降序排列取出给images变量；
    # images用于在render_template中传入参数，这就是jinja2模板语言了，传入的参数在html文件中继续应用，用于显示；
    # return render_template('index.html', images=images)
    # render_template是jinja2模板的用法(在class_02讲过)，即MVC的开发模式，调用HTML写好的页面做显示；直接显示.html中页面
    # 的样子，其中里面还加入了CSS的渲染等，这个就是前端做的任务了；

    # 将首页数据初始化为每页5张图，下面使用AJAX异步刷新的方式
    images = Image.query.order_by('id desc').paginate(1, 5, False)
    return render_template('index.html', images=images.items)


# 实现AJAX的关键函数，首页实现AJAX需要这个图片查询函数做辅助
@app.route('/images/<int:page_num>/<int:per_page>/')
def index_paginate(page_num, per_page):
    # 1.获取待查询的图片序列，每页获取5张；点一次更多就是1页；
    images = Image.query.order_by('id desc').paginate(page=page_num, per_page=per_page, error_out=False)
    # 2.设立标志位，即是否还有下张图
    map = {'has_next' : images.has_next}
    image = []
    # 3.将每张图所需的下面的几个信息存入image变量中
    for item in images.items:
        comment_user_username = []
        comment_user_id = []
        comment_content = []
        for comments_i in item.comments:
            comment_user_username.append(comments_i.users.username)
            comment_user_id.append(comments_i.users.id)
            comment_content.append(comments_i.content)

        imgov = {'image_user_id': item.users.id,
                 'image_user_head_url': item.users.head_url,
                 'image_user_username': item.users.username,
                 'image_id':item.id,
                 'image_url':item.url,
                 'image_comments_length':len(item.comments),
                 'comment_user_username': comment_user_username,
                 'comment_user_id':comment_user_id,
                 'comment_content':comment_content}

        image.append(imgov)
    # 4.将image存入map中，返回map的json串；用于前端显示每页的5张图；
    map['images'] = image
    return json.dumps(map)


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
def profile_paginate(user_id, page, per_page):
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



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                    旧版注册登录相关
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# flash message用的比较多，独立成一个函数；category为分类闪现的应用，具体可看下面资料：
# http://docs.jinkan.org/docs/flask/patterns/flashing.html
def redirect_with_msg(target, msg, category=''):
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
    # 实现next优化，登录/注册成功后返回之前的页面
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

    # 2.业务逻辑处理，看是否注册过该username，username/password是否存在等等异常判断
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
    # return redirect('/')  # 当登出之后自动重定向到首页
    return redirect('/wtf/login/')  # 新版的登出，即最终返回登录页，而不是首页



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                    新版注册登录相关
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 新版登录
@app.route('/wtf/login/', methods=['GET', 'POST'])
def wtf_login():
    # 1.获取登录表单，在登录表单中获取到了username,password，相当于旧版中的request.values
    form = LoginForm()
    # 2.将得到的用户名进行一系列判断
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        # 3.业务逻辑判断用户名是否存在
        if user is not None:
            m = hashlib.md5()
            m.update(form.password.data + user.salt)
            password = m.hexdigest()
            # 4.业务逻辑判断密码----这里用到了将提取到的密码进行md5加密然后与数据库中的密码进行比对的方法
            if password != user.password:
                return redirect_with_msg('/wtf/login/', u'密码不正确', 'login')
            # 最终则登录用户
            login_user(user)
            # 5.用户体验优化，即注册/登录完后可以跳回注册前点击的页面，而不是直接返回首页；这里用一个next变量即可实现
            next = request.args.get('next')
            if next != None:
                return redirect(request.args.get('next'))
            return redirect('/profile/' + unicode(user.id))
            flash('用户不存在.')
    return render_template('reglogin/reglogin_login.html', form = form)


# 新版注册
@app.route('/wtf/register/', methods=['GET', 'POST'])
def wtf_register():
    # 1.获取注册表单，从注册表单中将填入的数据得到存入form变量中，即username，password，email；相当于旧版注册中的request.values
    form = RegisterForm()
    # 2.业务逻辑处理，看是否出测过该username，username/password是否存在等等异常判断；这一个功能在forms.py中做的；
    if form.validate_on_submit():
        # 3.密码进行salt加密，即对md5的加密方式进行提高加密等级，增加一个字符串再进行MD5加密；
        salt = '.'.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 10))
        password = form.password.data
        m = hashlib.md5()
        m.update(password + salt)
        password = m.hexdigest()
        # 4.将新数据提交给数据库，最后要commit一下
        user = User(form.username.data, form.email.data, password, salt)
        db.session.add(user)
        db.session.commit()
        # 5.获取token，用于加密邮件认证链接防止被人破解；加入数据库后给用户发送邮件点击完成注册；
        token = user.generate_confirmation_token()
        send_email(form.email.data, u'Please activate your account', u'mail/new_user', user=user, token = token)
        # 6.注册好了之后自动登录
        login_user(user)
        # 7.用户体验优化，即注册/登录完后可以跳回注册前点击的页面，而不是直接返回首页；这里用一个next变量即可实现
        next = request.args.get('next')
        if next != None:
            return redirect(request.args.get('next'))
        # 8.最终将返回首页，重定向回首页
        return redirect('/profile/' + unicode(user.id))
    # 若form不在表单中，直接走模板会注册页
    return render_template('reglogin/reglogin_register.html', form = form)


# 在点击了邮件的认证链接后，通过url_for重定向回该函数的route参数，然后对点击的token进行confirm认证，看是否是该id的token；
@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.email_actived:
        return redirect('/')
    if current_user.confirm(token):  # 调用User类中的confirm函数，进行confirm认证是否是该id
        flash('your account has been activated')
    else:
        flash('your account has not been activated, something error')
    return redirect('/')


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                    上传图片相关
上传步骤：
    1.将上传的文件的信息通过request请求获取出来，保存在变量file中；
    2.将文件后缀名取出存入file_ext变量中；
    3.将图片提交至服务器之前，先对文件的后缀名做一个验证，看后缀名是否在配置文件允许范围之内;若符合，则将文件保存在服务
器，并获得一个URL地址；(调用sava_to_local函数，将上传的图片在本地保存,并返回一个可以访问的URL地址)；
    4.如果URL存在，则将该图存储到数据库当中；
    5.调用view_image函数，其实是flask的send_from_directory，上传图片之后，web需要显示；则此处添加一个图片显示函数；
    6.全部执行完后，将跳转回当前上传图片的用户的个人详情页去；
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 2.将上传的图片在本地保存,并返回一个可以访问的URL地址
def save_to_local(file, file_name):
    save_dir = app.config['UPLOAD_DIR']  # 获取根目录
    file.save(os.path.join(save_dir, file_name))  # 将上一步的根目录与文件名结合保存在本地的文件夹中
    return '/image/' + file_name  # 返回一个可以访问的URL地址，比如为/image/xxxx.jpeg


# 3.将上传的图片在七牛云存储，并返回一个可以访问的URL地址
def save_to_qiniu(file, file_name):
    return qiniu_upload_file(file, file_name)  # qiniusdk.py中函数，传入从post请求到的文件以及得出的文件名


# 4.上传图片之后，web需要显示；则此处添加一个图片显示函数；
@app.route('/image/<image_name>')
def view_image(image_name):
    # flask中集成了这么一个函数，send_from_directory；当用户直接访问该URL时，就直接显示该目录下的那个图；
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)


# 1.上传图片时需要调用的函数；这就是一个API接口，后端写好后，就算没有前端，用postman调试，也可以直接进行上次，入库等操作；
# upload上传内容必须要用post方法。为什么？
# get方法在请求头后面是不带任何参数的，即没有数据区；而post方法在请求的尾部是带上任何形式数据的。
@app.route('/upload/', methods=['POST'])
def upload():
    '''
    print request.files
    print type(request.files)
    print dir(file)
    打印看一下文件的目录信息，文件信息等，在后面提取关键字的时候使用。比如有如下信息：
    ['__bool__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattr__', '__getattribute__',
    '__hash__', '__init__', '__iter__', '__module__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__',
    '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parse_content_type', 'close',
    'content_length', 'content_type', 'filename', 'headers', 'mimetype', 'mimetype_params', 'name', 'save', 'stream']
    '''
    # 1.将上传的文件的信息通过request请求获取出来，保存在变量file中；files是请求提交过来时里面的一些文件；
    # []内是上传的文件定义的key名字。如果上传的多变量，比如还有file1,file2等，直接在这个dict里更改即可，可以提取file1,file2.
    file = request.files['file']
    # 2.将文件后缀名取出存入file_ext变量中；
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()  # 比如为xxx.bmp，则file_ext内容为bmp
    # 3.将图片提交至服务器之前，先对文件的后缀名做一个验证，看后缀名是否在配置文件允许范围之内;若符合，则将文件保存在服务器，并获得一个URL地址
    if file_ext in app.config['ALLOWED_EXT']:
        # 获得文件整体名字，为了防止名字中含有html等干扰信息，选择用一个uuid(通用唯一识别码，就是一个随机值)的方式代替真名字
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        # url = save_to_local(file, file_name)  # 调用写好的函数，将文件保存在本地，并获得一个URL地址
        url = save_to_qiniu(file, file_name)    # 调用写好的函数，将文件保存在服务器，并获得一个URL地址
        # 4.如果URL存在，则将该图加载到数据库当中
        if url != None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()
    # 5.如果上面某几步失败或者全部执行完后，将跳转回当前上传图片的用户的个人详情页去
    # return redirect('/profile/%d/' % current_user.id)
    return redirect_with_msg('/profile/%d/' % current_user.id, '图片上传成功')  # 打一个flash消息



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                图片详情页/首页增加评论
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 增加评论的URL，为何用post请求？
# Post，它是可以向服务器发送修改请求，从而修改服务器的，比方说，我们要在论坛上回贴、在博客上评论，这就要用到Post了，当然
# 它也是可以仅仅获取数据的。详情：https://zhidao.baidu.com/question/1759920971069677948.html
@app.route('/addcomment/', methods={'post'})
@login_required
def add_comment_to_pageDetail():
    # 1.获取Comment实例所需的属性
    image_id = int(request.values['image_id'])
    content = request.values['content']
    # 2.构造comment实例
    comment = Comment(content, image_id, current_user.id)
    # 3.将comment该条数据添加到Comment表中
    db.session.add(comment)
    db.session.commit()
    # 4.每页的评论信息存入map中，最终返回json格式用于前端显示
    return json.dumps\
    ({
        "code":0,
        "id":comment.id,
        "content":content,
        "username":comment.users.username,  # 因为Comment表与User表是多对多，relationship关系；
        "user_id":comment.users.id
     })