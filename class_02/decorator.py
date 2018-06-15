# coding=utf-8
# 装饰器补习
'''
# 1.函数对象有一个__name__属性，可以拿到函数的名字比如now()函数，即为now.__name__
# 2.为了增强now函数功能，但又不希望更改now定义，这种在代码运行期间动态增加功能的方式，称之为“装饰器”
# @log 即python中的装饰器，可以对程序中每句是否执行没有进行打log，相当于Java中的注解
# 将装饰器用于某个函数上时，要在函数定义前加上一个 @log
def log(func):
    def wrapper(*args, **kwargs):
        print 'call %s():' % func.__name__
        return func(*args, **kwargs)  # 执行func函数，即此时的hello函数，打印hello world

    return wrapper()


# 3.观察上面的log，因为它是一个decorator，所以接受一个函数作为参数，并返回一个函数。我们要借助Python的@语法，
# 把decorator置于函数的定义处：
@log
def now():
    print 'hello，world'


# 5.由于log()是一个decorator，返回一个函数，所以，原来的now()函数仍然存在，只是现在同名的now变量指向了新的函数，
# 于是调用now()将执行新函数，即在log()函数中返回的wrapper()函数。
# 6.wrapper()函数的参数定义是(*args, **kwargs)，因此，wrapper()函数可以接受任意参数的调用。在wrapper()函数内，首先打印日志，
# 再紧接着调用原始函数。
# *args 用来传递任意个无名子参数，这些参数会以一个Tuple的形式访问
# **kwargs  用来处理传递任意个有名字的参数，这些参数用dict来访问
'''


# 如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本:
# 相当于如果希望多打印一个参数的话，就在log函数处传入一个参数，只需要多嵌套一层就够了，其他的都是一样的
def log1(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print '%s %s():' % (text, func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator
# 剖析上面的语句，首先执行log('execute')，返回的是decorator函数，再调用返回的函数，参数是now函数，返回值最终是wrapper函数。

@log1('execute')
def now1():
    print '2018-06-12'


if __name__ == '__main__':
    # 4.调用now()函数，不仅会运行now()函数本身，还会在运行now()函数前打印一行日志：
    # now  # 注意这里的now后并没有()，不然会出bug； 相当于执行 log(now())
    now1()

'''
在面向对象（OOP）的设计模式中，decorator被称为装饰模式。OOP的装饰模式需要通过继承和组合来实现，而Python除了能支持
OOP的decorator外，直接从语法层次支持decorator。Python的decorator可以用函数实现，也可以用类实现。
decorator可以增强函数的功能，定义起来虽然有点复杂，但使用起来非常灵活和方便。
'''