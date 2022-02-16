from django.db import models

# Create your models here.
class User(models.Model):

    username = models.CharField("用户名", max_length=30, unique=True)
    password = models.CharField("密码", max_length=32)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
    user_email = models.CharField("邮箱", max_length=30, default="无")
    user_phone = models.CharField("手机", max_length=30, default="无")

    def __str__(self):
        return 'username %s' % (self.username)
