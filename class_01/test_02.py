# coding=utf-8
# 演示字符串
def demo_string():
    str1 = 'helloworld'
    str2 = '    \n\rhello world  \r\n'
    str3 = 'hello world'
    print 1, str1.capitalize()  # 输出首字母大写的字符串
    print 2, str1.replace('world', 'nowcoder')  # 替换
    print 3, str2.lstrip()  # 截掉字符串前面的空格
    print 4, str2.rstrip()  #
    print 5, str3.startswith('hel')  # 判断是否以'hel'开头
    print 6, str3.endswith('x')  # 判断是否已'x'结尾
    print 7, str1 + str2 + str3
    print 8, len(str3)  # 求长度
    print 9, '-'.join(['a', 'b', 'c'])  # 将dict中的字符以-连接起来
    print 10, str3.split(' ')  # 将str3中字符串根据空格分割开
    print 11, str3.find('ello')  # 找到该字符串在str3中出现的位置


# 演示运算符
def demo_operation():
    print 1, 1 + 2, 5 / 2
    print 2, True, not True
    print 3, 1 < 2, 5 < 2, 2 << 3, 5 | 3, 5 ^ 3


# 演示内置函数
def demo_buildingfunction():
    x = 2
    y = 3
    print 'a', x, y, type(x), type(y)  # 求元素类型
    print 'b', max(5, 3), min(2, 1)  # 大 小
    print 'c', len([1, 2, 3])  # 可以求数组，元祖，list，tuple等的长度
    print 'd', abs(-2)  # 求绝对值
    print 'e', range(1, 10, 3)  # 从1开始，到10结束，每次走3步
    print 'f', dir(list)  # dir打印list中的函数名，内部属性等等
    x = 2
    print 'g', eval('x + 3')  # 直接做加法运算
    print 'h', chr(97), ord('a')  # 将ASCII码97转化为字符 将字符转化为ASCII码
    print 'i', divmod(11, 3)  # 11/3 = 3...2


# 演示控制流if for while
def demo_controlflow():
    score = 65
    if score > 99:
        print 1, 'A'
    elif score > 60:
        print 2, 'B'

    while score < 100:
        print score
        score += 10

    # for loop演示
    socore = 65
    for i in range(0, 10, 2):  # i从0开始到10结束，步进为2；相当于C中的for(int i=0;i<=10;i+=2){print i};
        print i

    # continue break pass 演示
    for i in range(0, 10, 2):  # i<5则结束本次循环 i>8则结束所有循环
        if i < 5:
            continue
        if i > 8:
            break
        print i


# 演示python数据结构--list 用[]创建，相当于vector，下面有一系列的操作
def demo_list():
    # 1.相当于C++ 的vector
    list1 = [1, 2, 3]
    print list1
    # 2.python的list什么内容都可以存
    list2 = ['a', 'c', 1, 3, 1.1]
    print list2
    # 3.将list2接在list1后面
    list1.extend(list2)
    print list1
    # 4.
    print len(list1)
    # 5.判断'a'是否在list2中
    print 'a' in list2
    # 6.python中操作符重载本身就支持；将list1和list2链接起来
    list1 = list1 + list2
    print list1
    # 7.在list2的索引0前面加上'www'
    list2.insert(0, 'www')
    print list2
    # 8.将list2中索引1的元素弹出来
    list2.pop(1)
    print list2
    # 9.将list2逆序，在list2的基础上继续，直接在list2上更改
    list2.reverse()
    print list2
    # 10.直接按下标访问，想C++中的数组一样
    print list2[3]
    # 11.对list排序
    list2.sort()
    print list2
    # 12.相当于对容量扩充2倍，内容复制一份接在list2后面
    print list2 * 2


# 演示python数据结构--tuple(元祖) 就是不能改变值的list 用()创建
def demo_tuple():
    tuple1 = (1, 2, 3)  # 用()
    list1 = [1, 2, 3]  # 用[]
    list1.append(4)  # tuple则没有该功能，tuple是一个只读的，不可写入或改变操作
    print tuple1
    print list1


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


# 演示python数据结构--dict，就是相当于C++STL中的map hash_map ,即key-value的结构 用{key:value}创建
def demo_dict():
    # 1.相当于C++STL中的map hash_map ,即key-value的结构 用{key:value}创建
    dict1 = {4: 16, 1: 1, 2: 4, 3: 9}
    print dict1
    # 2.分别打印dict中的key value 打印出是list的形式
    print dict1.keys(), dict1.values()
    # 判断有无某个key
    print dict1.has_key(3), dict1.has_key('3')
    # 3.打印dict的键值对，一对一对的打印，一行一行的显示
    # 相当于C++中的 map<int,int>::iterator iter=map1.begin();for(;iter!=map1.end();iter++){print *iter};
    # 遍历key-value，并且按key从小到大的方式排序打印
    for key, value in dict1.items():
        print'key-value', key, value
    # 4.dict中的value可以为函数，可以在访问key的时候直接使用这个value函数;相当于C++中的函数指针
    dict2 = {'+': add, '-': sub}
    print dict2['+'](1, 2)
    print dict2.get('-')(5, 3)  # 效果一样
    # 5.pop弹出某个key-value对
    dict1.pop(4);
    print dict1
    # 6.del也是删除key，和pop功能一样，形式不同
    del dict1[1]
    print dict1


# 演示python数据结构--set，集合，用set((x,x...))声明，值不可改变，但是要在()前加上set，不然就变成tuple元组了；就是我们常说的集合，有一系列操作
def demo_set():
    # 1.声明set，用set((x,x...))声明;第一个()相当于set函数的(),第二个()相当于一个tuple构成的元组，第二个()也可以用[],
    # 也可以是一个变量list1，随便放，理解成set()函数内的一个参数即可。
    set1 = set([1, 2, 3])
    set2 = set((2, 3, 4))
    print set1
    # 2.给set添加key,set无value
    set1.add(4)
    print set1
    # 3.求set集合的交集，两种方式
    print set1.intersection(set2), set1 & set2
    # 4.求set集合的并集，两种方式
    print set1.union(set2), set1 | set2
    # 5.对set集合做减法运算，减去重复key
    print set1 - set2
    # 6.给set添加元素
    set1.add('x')
    print set1
    # 7.求set长度
    print len(set1)


if __name__ == '__main__':
    # demo_string()
    # demo_operation()
    # demo_buildingfunction()
    # demo_controlflow()
    # 数据结构：list tuple dict set
    # demo_list()
    # demo_tuple()
    # demo_dict()
    demo_set()
