from django.db import models
from user.models import User

# Create your models here.
# 笔记表
class Note(models.Model):
    title = models.CharField('标题', max_length=100)
    link = models.CharField('链接', max_length=50, default="无")
    content = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.title)
