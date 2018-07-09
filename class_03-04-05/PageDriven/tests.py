# -*- encoding=UTF-8 -*-
# 放单元测试函数的文件
import unittest
from nowstagram import app

# 测试用例类
class NowstagrmTest(unittest.TestCase):
    # 每次跑单元测试的时候都会跑，用于初始化测试数据
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()  # 获得测试所需的实例app
        print 'setUp'

    # 清理测试数据
    def tearDown(self):
        print 'teardown'
        pass

    # 模拟注册函数，其实就是仿照postman；对注册函数使用post请求，看返回码是否符合；
    def register(self, username, password):
        return self.app.post('/reg/', data={"username":username, "password":password}, follow_redirects=True)

    # 模拟登录函数
    def login(self, username, password):
        return self.app.post('/login/', data={"username": username, "password": password}, follow_redirects=True)

    # 模拟登出函数
    def logout(self):
        return self.app.get('/logout/')

    # 测试函数，测试注册登录登出
    def test_reg_logout_login(self):
        assert self.register("hello", "world").status_code == 200  # 测试是否为200的status_code
        assert '-hello' in self.app.open('/').data  # 测试注册的用户hello是否在数据库中
        self.logout()
        assert '-hello' not in self.app.open('/').data  # 各种测试，总之就是考虑全面，才能保证测试的完整性
        self.login("hello", "world")
        assert '-hello' in self.app.open('/').data
