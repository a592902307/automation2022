# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/6/2 15:11
@file:plan.py
@desc:
'''

from django.conf import settings
from django.db import models

from .base import CommonInfo
from .hr3 import Case
from .mgr import Environment

class Plan(CommonInfo):
    status_choice={
        (0,'未执行'),
        (1,'执行中'),
        (2,'中断'),
        (3,'已执行')
    }
    cases=models.ManyToManyField(Case,blank=True,verbose_name="测试用例")
    executor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,null=True,verbose_name="执行者")
    environment=models.ForeignKey(Environment,on_delete=models.SET_NULL,null=True,verbose_name="测试环境")
    name=models.CharField(max_length=32,unique=True,verbose_name="计划名称")
    status=models.SmallIntegerField(choices=status_choice,default=0,verbose_name="计划状态")
    exec_counts=models.PositiveSmallIntegerField(default=0,verbose_name="执行次数")

class Report(CommonInfo):
    plan=models.ForeignKey(Plan,on_delete=models.DO_NOTHING,related_name='reports')
    path=models.CharField(max_length=500,verbose_name='报告路径')
    detail=models.TextField(verbose_name='报告详情')
    # 执行人
    trigger=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,null=True)