# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/2/6 13:17
@file:base.py
@desc:
'''

from django.db import models
from django.conf import settings

# 公共，模型
class CommonInfo(models.Model):
    # auto_now_add使用当前时间，不更新; auto_now使用当前时间，数据被更新后时间会随之更新
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True,null=True)
    update_time=models.DateTimeField(verbose_name="更新时间",auto_now=True)
    # nul =True 代表该字段可以不写，数据库给你存一个空字符串
    # blank=True 表示该字段可以为空，但必须写
    desc=models.TextField(verbose_name="描述",null=True,blank=True)

    # 创建者
    create_by=models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET_NULL,null=True,verbose_name='创建者',
                                  related_name='%(class)s_create_by')
    # 更新者
    update_by=models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET_NULL,null=True,verbose_name='更新者',
                                  related_name='%(class)s_update_by')

    def __str__(self):
        # 检查当前对象是否有name属性
        if hasattr(self,'name'):
            return self.name
        return self.desc
    class Meta:
        # abstract表示定义为抽象表，不会创建数据库表  ordering表示默认排序
        # abstract不会被子类继承，子类需要自己显示定义
        abstract=True
        ordering=['id']
