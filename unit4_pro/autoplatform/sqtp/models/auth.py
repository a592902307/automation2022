# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/2/7 23:09
@file:auth.py
@desc:
'''

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE=(
        (0,'开发'),
        (1,'测试'),
        (2,'运维'),
        (3,'项目经理'),
    )
    realname=models.CharField(verbose_name='真实姓名',max_length=32)
    phone=models.CharField(verbose_name='手机号',max_length=11,unique=True,null=True,blank=True)
    user_type=models.SmallIntegerField(verbose_name='用户类型',choices=USER_TYPE,default=1)
