# coding=utf-8

def demo_exception():
    try:
        print 2 / 1
        print 2 / 0
        # 这个属于主动抛出异常，就算2/1没有错误，到了这也会抛出异常，平常的主动捕获异常这里是不需要的；经常用于类型检测到
        # xx时主动抛出一个异常
        raise Exception('Raise Error', 'Nowcoder')
    # 这个属于检测到了异常，比如2/0是不对的，则2/0后面的都不执行了，直接自动捕获到了该异常然后跳入except Exception中，
    # 并输出错误类型，最终在执行finally
    except Exception as e:
        # 通常在这里要打log文件，查看错误的原因等等
        print 'error:', e  # 输出错误
    finally:  # 不管这个代码块有没有异常，这个finally的部分都会执行，常用于打开文件后进行关闭等等
        print 'clean up'


if __name__ == '__main__':
    demo_exception()
