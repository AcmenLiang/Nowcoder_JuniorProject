# -*- encoding=UTF-8 -*-
# 文件功能：将app中页面的功能写好。视图写在这。

from nowstagram import app, db  # 从application中导入app，不然找不到该模块；从__init__中导入是不行的！！！必须从子目录中导入！！！
from models import User, Image, Comment  # 由于view与model文件在泳衣目录，故直接这么导入即可，将这3个类导入；
from flask import render_template, redirect


# python的装饰器，传入一个/就可以直接下面的函数，注意URL不是localhost/index，index只是个函数；这里就是127.0.0.1:5001/
@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    # 查询Image类(表)中的图，查出10张来，按图片id的降序排列取出给images变量；
    # images用于在render_template中传入参数，这就是jinja2模板语言了，传入的参数在html文件中继续应用，用于显示；
    return render_template('index.html', images=images)
    # render_template是jinja2模板的用法(在class_02讲过)，即MVC的开发模式，调用HTML写好的页面做显示；直接显示.html中页面
    # 的样子，其中里面还加入了CSS的渲染等，这个就是前端做的任务了；


# 图片详情页的开发，URL为127.0.0.1:5001/image/图片id ；<int:image_id> 对route传入参数，相当于传入形参，以前讲过；
@app.route('/image/<int:image_id>/')
def image(image_id):
    image = Image.query.get(image_id)  #用的单数，就一张图片，获取到了图片的变量
    if image == None:
        return redirect('/')  # 重定向的页面跳转，在class_02讲过；如果图片为空，则重定向回首页；
    comments = Comment.query.filter_by(image_id=image_id).order_by(db.desc(Comment.id)).limit(20).all()
    return render_template('pageDetail.html', image=image, comments=comments)  # 否则就进入图片详情页；传入.html网页作为模板


# 意思都和上面差不多，就不多写了
@app.route('/profile/<int:user_id>/')
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    return render_template('profile.html', user=user)