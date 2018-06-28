# -*- encoding=UTF-8 -*-
'''
文件功能：对应数据库中的各个表的类写在该文件中；比如User类就是数据库中的users表；所有类的基类叫做db.Model，
它存储在您必须创建的 SQLAlchemy 实例上。
'''

from nowstagram import db
from datetime import datetime
import random


# 对应数据库中的users表
class User(db.Model):
    __tablename__ = 'users'  # model类下面的属性，更改表的名字
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # primary_key=True表示将id设为主键，即id值是唯一标识；autoincrement=True表示该列的id生成的序号是自己产生，且是自增的；
    # 即id这个键的值不需要初始化了(__init__函数不需要再写id的初始化内容)，加上了autoincrement后就会从1开始自增，直至不
    # 在session.add数据为止；

    username = db.Column(db.String(80), unique=True)  # unique=True指这个字段在这列里不能重复
    password = db.Column(db.String(32))  # Column代表数据库中的一列，即关键字
    head_url = db.Column(db.String(256))
    images = db.relationship('Image', backref='users', lazy='dynamic')
    # 含义解释：将两个表(User与Image)关联起来了，表示User中的image是从Image类来的；
    '''
    1.一对多查询，解释backref的作用：
    user = User.query.get(10)  # 获取User类中主键id=10的用户变量
    print 'test10', user, user.images.all()  # 查询出来如果有很多数据的话，要加上all()，不然会打出一些SQL语句来；
    # 打印跟id=10相关联的所有image，之所有能实现，是在User类中将images与User关联起来了，用的relationship，即一对多的概念；
    image = Image.query.get(35)  # 查询图片id为35的变量
    print 'test11', image, image.user_id  # 这里是用的Image类中的变量，即user_id，即发图片的是哪个人
    # 这里要在User类中将User类与Image类关联的时候(relationship语句中)，加上backref='users'，表示反关联，即双向关联，这样也就能
    # 根据图片的id查询到人的id了；上面两个print语句就是表示了双向关联可以互相查询的意思；
    2.解释lazy的作用：
    lazy='dynamic' lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据；具体参数优化可见：
    https://blog.csdn.net/bestallen/article/details/52551579
    '''
    # relationship中的第一个参数是要关联的类(表)的名称，这位类名Image，而不是__tablename__的images；
    # 表示一个人有很多图片，即users类中的主键id可以对应许多images，即一对多的关系，用relationgship关联；
    # ForeignKey仅仅是取其他表中键的值，而并非关联起来，是表1的id用了表2的id，则用ForeignKey拷过来；若是关联，则用relationship

    # __init__相当于构造函数，声明一个实例的时候会通过这里进行属性的初始化；self即相当于this指针
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'  # 随机生成头像的一种方式

    # 这里打印出来的格式就是User类中__repr__函数的格式，比如User类中是return '[User %d %s]' % (self.id, self.username)
    # 则就是打印出的[User 3 牛客3]， __repr__就是用于查询User.query()函数要查询的东西的内容及格式。
    def __repr__(self):
        return '[User %d %s]' % (self.id, self.username)


# 每个人都可能发表若干张图片，此类对应数据库中的images表
class Image(db.Model):
    __tablename__ = 'images'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 图片的ID，主键
    url = db.Column(db.String(512))  # 图片的URL地址
    created_date = db.Column(db.DateTime)  # 图片发表时间，用DateTime数据类型

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # ForeignKey仅仅是取其他表中键的值，而并非关联起来，是表1的id用了表2的id，则用ForeignKey拷过来；若是关联，则用relationship
    # 图片是那个用户ID发表的，则images表中的user_id是用users表中的id来的；他们有关联性，这是ORM的好处；
    # users的id是主键，users是id的主键表；images相对于users中的id来说是外键表；
    # 想让主键表中的键值直接过来用ForeignKey函数来实现；

    comments=db.relationship('Comment')
    # 含义解释：将两个表(Image与Comment)关联起来了，表示Image中的comments是从Comment类来的；
    # 表示一个图片(当前的类/表)有很多评论(要关联的东西)，即Image类中的主键id可以对应许多comments，即一对多的关系，用relationgship关联；
    # ForeignKey仅仅是取其他表中键的值，而并非关联起来，是表1的id用了表2的id，则用ForeignKey拷过来；若是关联，则用relationship

    # 构造函数
    def __init__(self, url, user_id):
        self.url = url
        self.created_date = datetime.now()
        self.user_id = user_id

    # 查询函数(Image.query())数据查询后的内容和格式就是__repr__函数定义的，比如这里查询出来的只有图片id 图片url；
    def __repr__(self):
        return '[Image %d %s]' % (self.id, self.url)


# 每张图片下都可能有若干条评论；此类对应数据库中的comments表；
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 评论的ID，设为主键
    content = db.Column(db.String(1024))  # 评论内容
    status = db.Column(db.Integer, default=0)  # 评论的状态，0表示正常，1表示被删除；默认为0
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 该评论是哪个人(users.id)评论的，跟users表中的主键id有关联，需要用到users.id的值，则用ForeignKey函数；类似于某个表
    # 的某个键值需要用到其他表的键值时，就要用ForeignKey这样的函数；比如上面的images.id需要用到users.id一个道理；
    # ForeignKey仅仅是取其他表中键的值，而并非关联起来，是表1的id用了表2的id，则用ForeignKey拷过来；若是关联，则用relationship

    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    # ForeignKey仅仅是取其他表中键的值，而并非关联起来，是表1的id用了表2的id，则用ForeignKey拷过来；若是关联，则用relationship
    # 该评论是评给哪个图的，跟上面一个道理，需要关联images.id中的键值，要用ForeignKey函数进行取images.id中的值；
    # 即comments.image_id跟images.id关联起来了；

    users=db.relationship('User')
    # 含义解释：将两个表(Comment与User)关联起来了，表示Comment中的users是从User类来的；
    # 表示一个评论(当前的类/表)要跟User(要关联的东西)关联起来，用relationgship关联；
    # ForeignKey仅仅是取其他表中键的值，而并非关联起来，是表1的id用了表2的id，则用ForeignKey拷过来；若是关联，则用relationship

    # 构造函数
    def __init__(self, content, image_id, user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    # 查询函数(Comment.query())数据查询后的内容和格式就是__repr__函数定义的，比如这里查询出来的只有评论id 和 评论内容；
    def __repr__(self):
        return '[Comment %d %s]' % (self.id, self.content)
