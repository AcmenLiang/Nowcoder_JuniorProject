# -*- encoding=UTF-8 -*-
# 文件功能：对应数据库中的各个表的类写在该文件中；比如User类就是数据库中的users表；


from nowstagram import db


# 所有类的基类叫做db.Model，它存储在您必须创建的 SQLAlchemy 实例上。


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary_key=True表示将id设为主键，即id值是唯一标识；
    # autoincrement=True表示该列的id生成的序号是自己产生，且是自增的
    username = db.Column(db.String(80), unique=True)  # unique=True指这个字段在这列里不能重复
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '[User %d %s]' % (self.id, self.username)
