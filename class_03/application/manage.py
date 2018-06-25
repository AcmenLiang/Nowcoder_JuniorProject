# -*- encoding=UTF-8 -*-
# 文件功能：外部的脚本控制文件，做一些数据库初始化，跑些任务等等；
from application import app
from flask_script import Manager

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
