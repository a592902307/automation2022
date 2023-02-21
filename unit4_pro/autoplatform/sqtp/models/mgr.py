# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/2/6 11:25
@file:mgr.py
@desc:
'''

from django.db import models
from .base import CommonInfo
from django.conf import settings

class Project(CommonInfo):
    pro_status=(
        (0,'开发中'),
        (1,'维护中'),
        (2,'稳定运行')
    )
    # 管理员
    admin=models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,null=True,verbose_name="项目管理员",related_name="project_admin")
    # 成员
    members=models.ManyToManyField(settings.AUTH_USER_MODEL,verbose_name="项目成员",related_name="project_members")

    name=models.CharField(verbose_name="项目名称",max_length=32,unique=True)
    status=models.SmallIntegerField(verbose_name="项目状态",choices=pro_status,default=2)
    version=models.CharField(verbose_name="版本",max_length=32,default="v1.0")

    # 子类要设置自己的Meta属性，则需要继承并扩展基类的Meta
    class Meta(CommonInfo.Meta):
        verbose_name="项目表"

class Environment(CommonInfo):
    # 服务类类型选项
    service_type=(
        (0,'web服务器'),
        (1,'数据库服务器')
    )
    # 服务器操作系统选项
    service_os=(
        (0,'window'),
        (1,'linux')
    )
    # 服务器状态选项
    service_status=(
        (0,'active'),
        (1,'disable')
    )
    project=models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name="所属项目")
    # ip--使用djangoORM提供的一个叫GenericIPAddressField专门储存IP类型的字段
    ip=models.GenericIPAddressField(verbose_name="ip地址",default="127.0.0.1")
    port=models.SmallIntegerField(verbose_name="端口号",default=80)
    category=models.SmallIntegerField(verbose_name="服务器类型",default=0,choices=service_type)
    os=models.SmallIntegerField(verbose_name="服务器操作系统",default=0,choices=service_os)
    status=models.SmallIntegerField(verbose_name="服务器状态",default=0,choices=service_status)

    def __str__(self):
        return self.ip+':'+self.port

    class Meta(CommonInfo.Meta):
        verbose_name="测试环境表"