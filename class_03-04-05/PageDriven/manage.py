# -*- encoding=UTF-8 -*-
# 文件功能：外部的脚本控制文件，做一些数据库初始化，跑些任务等等；仅仅是测试的时候用，对mysql中的数据进行增删改查，先建
# 立一些假数据，在web页面开发的时候能显示出来；在真正上线的时候，就会剥离这个，让数据库动态的run起来；
from nowstagram import app, db
from nowstagram.models import User, Image, Comment
from flask_script import Manager
from sqlalchemy import or_, and_
import random

manager = Manager(app)  # 声明脚本Manager的实例manager


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


# ORM好处，将数据库的操作用面向对象的python语言表达出来，通过python语言来操作数据库的增删改查，而不必去底层实现；
@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    # 100个用户，每个用户3张图片，每张图片3条评论
    for user_i_id in range(0, 100):
        db.session.add(User(u'牛客' + str(user_i_id + 1), 'password' + str(random.randint(0, 1000)))) # id从1开始
        for image_j_id in range(0, 10):
            # 看Image类中的构造函数__init__的参数是几个，这里就传入几个，相当于类的实例化(或者说是表中一条数据的建立)
            # 第2个参数就是用的user_id，故从上面的遍历中直接传下来
            db.session.add(Image(get_image_url(), user_i_id + 1))
            for comment_k_id in range(0, 3):
                db.session.add(Comment(u'这是一条评论：' + str(comment_k_id), 1 + 10 * user_i_id + image_j_id, user_i_id + 1))
                # 后面两个是image_id user_id，需要计算一下才是对应当前评论id的正确值；
    db.session.commit()  # 将数据插入后，需要commit一下，才能将数据真正的提交的数据库中；
    '''
    # 3.更新数据库中数据
    # (1)更新方式1：将id为50-100 步进为2的id的username前加上New1，通过给username赋值的方式来更新；
    for user_i_id in range(50, 100, 2):
        user = User.query.get(user_i_id)
        user.username = '[New1]' + user.username
    # (2)更新方式2：将User表中id=50的数据的username更新为New2，通过update的方式来更新；
    User.query.filter_by(id = 50).update({'username':'[New2]'})
        # update存的是dict的形式，即key为表中的关键字(如id,username等)，value为重置的数据；
    db.session.commit()  # 提交给数据库；
    # 4.删除数据库中数据
    for comment_k_id in range(50, 100, 2):
        comment = Comment.query.get(comment_k_id+1)
        db.session.delete(comment)
        # 删除方式一：用db.session.delete()；进入数据库发现Comment类中id为51 53 55...的那一行行数据都没了；
    Comment.query.filter_by(id = 30).delete()
    # 删除方式二：用query.delete()；删除数据库中Comment类中id为30的那一行数据；
    db.session.commit()  # 但凡是更新过数据库，就要commit一下；
    # 5.增加数据库中数据
    # 不举例了，上面的db.session.add(User(xxx))就是增加数据的例子；用add去增加新数据；
    '''
'''
# 1.查询
# 查询语句实例  User类是继承的SQLAlchemy的model类，model类中有query等一系列方法，所以这里可以之间用'.'来访问
# 这里打印出来的格式就是User类中__repr__函数的格式，比如User类中是return '[User %d %s]' % (self.id, self.username)
# 则就是打印出的[User 3 牛客3]， __repr__就是用于查询函数要查询的东西的内容及格式。
print 'test1', User.query.all()  # 表示查询users表的所有
print 'test2', User.query.get(3)  # 查询users表中主键为3的数据
print 'test3', User.query.filter_by(id=5).first()  # filter_by限制条件，即限制id=5；first表示id=5的第一条数据
print 'test4', User.query.order_by(User.id.desc()).offset(1).limit(2).all()
# order_by表示对数据集排序；desc表示降序排列；offset表示偏移1个，即从第2个开始；limit表示只要2个；all表示查到的所有的都打出来；
# 这句相当于SQL语句的：select * from users order by id desc limit 1,2  这就是ORM的好处，建立数据库与对象之间的一一映射。
print 'test5', User.query.filter(User.username.endswith('0')).limit(3).all()
# filter表示限制条件，此处条件（endswith）为User类中的表为username字段的结尾为'0'的数据；limit限制为3个；all表示所有的都打出来；
# 其实不加all的话就变成输出的是SQL语句的形式，即在MySQL等软件中也可以操作的语句；
print 'test6', User.query.filter(or_(User.id == 88, User.id == 99)).all()
# or_是sqlalchemy中的一个实例或类，用于限制条件的或链接，即filter限制id=88或id=99的数据；
print 'test7', User.query.filter(and_(User.id > 88, User.id < 93)).all()
# and_同理，就是与的意思，对限制条件进行与，同时符合；
print 'test8', User.query.filter(and_(User.id > 88, User.id < 93)).first_or_404()
# 查询条件同上，first_or_404表示返回查询的第一个结果,如果没有结果,则终止请求,返回 404 错误响应
print 'test9', User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items
# ordr_by是逆序一下，上面用过，随便组合；paginate表示对查询的数据分页，即此处的每页10条数据，找出第1页的来；items即将数据提出来，不然只是数据的位置而不是具体内容；
'''
'''
# 2.一对多/多对多查询(相当于查询两个表相关联的数据，比如跟user_id相关的image等)
user = User.query.get(10)  # 获取User类中主键id=10的用户变量
print 'test10', user, user.images.all()  # 查询出来如果有很多数据的话，要加上all()，不然会打出一些SQL语句来；
# 打印跟id=10相关联的所有image，之所有能实现，是在User类中将images与User关联起来了，用的relationship，即一对多的概念；
image = Image.query.get(35)  # 查询图片id为35的变量
print 'test11', image, image.user_id  # 这里是用的Image类中的变量，即user_id，即发图片的是哪个人
# 这里要在User类中将User类与Image类关联的时候(relationship语句中)，加上backref='users'，表示反关联，即双向关联，这样也就能
# 根据图片的id查询到人的id了；上面两个print语句就是表示了双向关联可以互相查询的意思；
'''

if __name__ == '__main__':
    # 这里只是先run一下，对mysql中的数据进行增删改查，先建立一些假数据，在web页面开发的时候能显示出来；在真正上线的时候，
    # 就会剥离这个，让数据库动态的run起来；
    manager.run()
