# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/2/6 11:25
@file:hr3.py
@desc:
'''

from django.db import models
from .mgr import Project
from .base import CommonInfo

# 测试平台核心模型----拆解HR用例部分

class Config(CommonInfo):
    project=models.ForeignKey(Project,on_delete=models.DO_NOTHING,null=True)
    name=models.CharField(verbose_name="用例名称",max_length=128)
    base_url=models.CharField(verbose_name="IP",max_length=512,blank=True,null=True)
    variables=models.JSONField(verbose_name="用例变量",null=True)
    parameters=models.JSONField(verbose_name="全局参数",null=True)
    verify=models.BooleanField(verbose_name='https校验',default=False)
    export=models.JSONField(verbose_name="用例返回值",null=True)

    # 模型元类，为模型增加额外的信息
    class Meta:
        ordering=['id']

class Case(CommonInfo):
    config=models.OneToOneField(Config,on_delete=models.DO_NOTHING)
    file_path=models.CharField(verbose_name="用例文件路径",max_length=1000,default='demo_case.json')
    def __str__(self):
        return self.config.name

    class Meta:
        ordering=['id']

class Step(CommonInfo):
    # 同个模型中，两个字段关联同一个模型，必须指定related_name，且名字不能相同
    # 归属用例
    belong_case=models.ForeignKey(Case,on_delete=models.CASCADE,related_name='teststeps')
    # 引用用例
    linked_case=models.ForeignKey(Case,on_delete=models.SET_NULL,null=True,related_name='linked_steps')
    name=models.CharField(verbose_name="步骤名称",max_length=128)
    variables=models.JSONField(verbose_name="步骤变量",null=True)
    extract=models.JSONField(verbose_name="请求返回值",null=True)
    validate=models.JSONField(verbose_name="结果校验",null=True)
    setup_hooks=models.JSONField(verbose_name="初始化",null=True)
    teardown_hooks=models.JSONField(verbose_name="清除",null=True)
    sorted_no=models.PositiveSmallIntegerField(verbose_name="步骤顺序",default=1)

    class Meta:
        ordering=['id','sorted_no']
        # 同一个用例的步骤顺序应该是不一样的
        unique_together=['belong_case','sorted_no']

class Request(CommonInfo):
    method_choices=( # method可选的字段，
        (0,'GET'),   # 参数1:实际存储在数据库中的值, 参数2：对外显示的值
        (1,'POST'),
        (2,'PUT'),
        (3,'DELETE'),
    )
    step=models.OneToOneField(Step,on_delete=models.CASCADE,null=True,related_name='request')
    method=models.SmallIntegerField(verbose_name="请求方法",choices=method_choices,default=0)
    url=models.CharField(verbose_name="请求路径",default='/',max_length=1000)
    params=models.JSONField(verbose_name="url参数",null=True)
    headers=models.JSONField(verbose_name="请求头",null=True)
    cookies=models.JSONField(verbose_name="Cookies",null=True)
    data=models.JSONField(verbose_name="表单参数",null=True)
    json=models.JSONField(verbose_name="json参数",null=True)
    def __str__(self):
        return self.url

    class Meta:
        ordering=['id']
