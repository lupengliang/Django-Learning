from django.test import TestCase
from django.urls import reverse


# 用来测试用户登录、注册
class UserTests(TestCase):
    """
    用来测试用户登录、注册
    """

    # 测试注册用户功能
    def test_register_user(self):
        """
        测试注册用户功能
        :version: 1.0
        :author: lupengliang
        :date: 2021-12-19
        :return:
        """
        response = self.client.get(reverse('user:reg_view'))
        print(response)

    # 测试登录功能
    def test_login_function(self):
        """
        测试登录功能
        :version: 1.0
        :author: lupengliang
        :date: 2021-12-19
        :return:
        """
        pass

    # 测试退出功能
    def test_logout_function(self):
        """
        测试退出功能
        :author: lupengliang
        :date: 2021-12-19
        :return:
        """
        pass
