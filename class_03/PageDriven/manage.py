# -*- encoding=UTF-8 -*-
# 文件功能：外部的脚本控制文件，做一些数据库初始化，跑些任务等等；
from nowstagram import app, db
from flask_script import Manager
from nowstagram.models import User

manager = Manager(app)


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('牛客' + str(i), 'password' + str(i)))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
