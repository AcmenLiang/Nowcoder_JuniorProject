# coding=utf-8
# 封装：把所有的属性方法集合在一起，集合在一个类中
# 继承：把基类中已有的东西继承下来，不需要重复定义
# 多态：方法的重载，根据传入参数的不同，执行相同的函数名却有不同的效果

# 类，封装
class User:
    type = 'USER'

    # 成员函数，这里是初始化函数（相当于C++的构造函数）
    def __init__(self, name, uid):
        self.name = name;
        self.uid = uid

    # 成员函数
    def __repr__(self):
        return 'im' + self.name + ' ' + str(self.uid)


# Admin类继承自User类
class Admin(User):
    # 类型是ADMIN
    type = 'ADMIN'

    # 比基类多了一个成员变量group
    def __init__(self, name, uid, group):
        User.__init__(self, name, uid)  # 调用基类函数来初始化
        self.group = group

    # 重载了基类函数，相当于实现了多态，根据传入参数不同，执行不同类中的函数，即多态；多了一个打印group
    def __repr__(self):
        return 'im' + self.name + ' ' + str(self.uid) + ' ' + self.group


if __name__ == '__main__':
    user1 = User('u1', 1)
    print user1
    admin1 = Admin('a1', 101, 'g1')
    print admin1
