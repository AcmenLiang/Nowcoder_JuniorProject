# -*- encoding=UTF-8 -*-
# flask-script 测试

from flask_script import Manager
from test_07 import app

'''
    创建并运行命令。创建一个Python模板运行命令脚本，可起名为test_08_manager.py
    在该文件中，必须有一个Manager实例，Manager类追踪所有在命令行中调用的命令和处理过程的调用运行情况。Manager只有一个参
数——Flask实例，也可以是一个函数或其他的返回Flask实例
'''
manager = Manager(app)

# 其次，创建并加入命令；有三种方法创建命令，即创建Command子类、使用@command修饰符、使用@option修饰符；

# 第一种——创建Command子类，Command子类必须定义一个run方法；
'''
创建Hello命令，并将Hello命令加入Manager实例；

from flask_script import Manager  
from flask_script import Command  
from debug import app  
  
manager = Manager(app)  
  
class Hello(Command):  
    'hello world'  
    def run(self):  
        print 'hello world'  
  
manager.add_command('hello', Hello())  
  
if __name__ == '__main__':  
    manager.run()
    
运行：python manager.py hello
'''


# 第二种——使用Command实例的@command修饰符
# 该方法创建命令的运行方式和Command类创建的运行方式相同； python test_08_manager.py hello
@manager.command
def initialize_database():
    'initialize database'
    print 'database...'


# 第三种——使用Command实例的@option修饰符
# 复杂情况下，建议使用@option；可以有多个@option选项参数；
# 运行方式：test_08_manager.py hello -n haoliang
@manager.option('-n', '--name', dest='name', default='nowcoder')
def hello(name):
    print 'hello', name


if __name__ == '__main__':
    # 调用manager.run()启动Manager实例接收命令行中的命令
    manager.run()
#   运行后，在命令行中指向test_08_manager.py -?可以看到允许执行的命令；比如本例子可以执行test_08_manager.py hello
# 函数，以及initialize_database函数；把这些函数用flask-script做成脚本即可。
#   等网站做大了，后面会有数据库的初始化，初始导入等等，那些东西写在哪里呢？一把就会采用脚本，将这些工作写在脚本中。
# 下节课就会把所有工作，初始化的工作啊，数据导入啊，清理啊，所有脚本要用到的东西，都会写在这个文件中，慢慢填充。
