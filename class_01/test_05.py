# coding=utf-8
# 随机数 和 正则表达式
import random
import re


# 随机数操作演示
# random.random     random.seed     random.randint      random.choice      random.sample
def demo_random():
    # 1.设置随机种子，若种子确定后，每次产生的随机数都是固定的
    # random.seed(1)
    # 2.输出0-1之间的浮点数
    print random.random()
    # 3.输出0-100之间的浮点数
    print random.random() * 100
    # 4.输出0-100之间的整数
    print int(random.random() * 100)
    # 5.输出0-200之间的整数
    print random.randint(0, 200)
    # 6.选择一个随机数，0-100之间，step为10，这样的随机数选一个
    print random.choice(range(0, 100, 10))
    # 7.选择一个随机序列(抽样)，这个随机序列有4个数，范围是0-100，step为5
    print random.sample(range(0, 100, 5), 4)
    # 8.random.shuffle对一个list进行随机打乱
    test1 = [1, 2, 3, 4, 5]
    random.shuffle(test1)
    print test1


# 正则表达式操作演示
# (a):\d 数字 \D非数字   \s 空格呀，-r呀，-t呀 \S 非xxx  \w a-z 0-9都是 \W 非w...
# (b):+ 表示至少匹配一次或一次以上      * 表示匹配0次或0次以上    ？表示只能匹配0次或1次
# (c):| 表示或   ^ 表示取反
# (d):() 即指定找的部分，默认都加()，加上()表示只要()内的部分
# (e):\\ 转义字符
# 正则表达式用在提取邮箱，网页的时间等等，删选某种格式的字符串，比如时间2016-09-11 就可以设定某种正则表达式
# 来选取特定的该时间，用于爬虫等等。
# Python 正则表达式 http://www.runoob.com/python/python-reg-expressions.html
#### re.match 尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回none；
#### re.search 扫描整个字符串并返回第一个成功的匹配
#### re.sub用于替换字符串中的匹配项
#### re.compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search() 这两个函数使用
#### re.findall 在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表
#### re.finditer 在字符串中找到正则表达式所匹配的所有子串，并把它们作为一个迭代器返回
#### re.spilt 按照能够匹配的子串将字符串分割后返回列表
def demo_re():
    # 匹配出str中数字
    str1 = 'abc123def12gh16'
    # compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search() 这两个函数使用
    p1 = re.compile('[\d]+')  # 匹配多个数字
    p2 = re.compile('[\d]')  # 匹配1个数字
    # findall在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表。
    # match 和 search 是匹配一次 findall 匹配所有。
    print p1.findall(str1)
    print p2.findall(str1)

    # 匹配出163邮箱
    str2 = 'a@163.com; b@qq.com; c@gmail.com; d@163.com; e@qq.com'
    p3 = re.compile('[\w]+@163\.com')  # w 表示所有0-9 a-z       + 表示多个    \.相当于转义字符，就是一个.
    p4 = re.compile('[\w]+@[163|qq]+\.com')  # 用一个|（或）匹配163或者qq邮箱，记得在[]外加上+ 表示多个
    print p3.findall(str2)
    print p4.findall(str2)

    # 匹配HTML字符串里的title body等等
    str3 = '<html><h>title</h><body>xxx</body></html>'
    p5 = re.compile('<h>[^<]+</h>')  # 直至找到不是<为止即str3中的title，相当于解析URL，提取出title来
    p6 = re.compile('<h>([^<]+)</h>')  # 在[^<]+外加上(),就只提取这里面的东西；
    p7 = re.compile('<h>([^<]+)</h><body>([^<]+)</body>')  # 当提取多个东西的时候就有用了，比如这里只提取出title和body，其他东西就不要了
    print p5.findall(str3)
    print p6.findall(str3)
    print p7.findall(str3)


if __name__ == '__main__':
    # demo_random()
    demo_re()
