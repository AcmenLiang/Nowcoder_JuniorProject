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


if __name__ == '__main__':
    print 'hello111'
    # demo_string()
    # demo_operation()
    # demo_buildingfunction()
    demo_controlflow()
