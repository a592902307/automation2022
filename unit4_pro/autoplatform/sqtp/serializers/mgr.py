# encoding: utf-8
'''
@author:yh
@contact:592902307@qq.com
@time:2023/3/2 13:47
@file:mgr.py
@desc:
'''

from rest_framework import serializers
from sqtp.models import Project,Environment
from sqtp.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # write_only=True 表示只做为入参传入，序列化后不作为出参传出去
    admin_id=serializers.IntegerField(write_only=True)
    admin=UserSerializer(read_only=True)
    create_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    update_time=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    class Meta:
        model=Project
        # fields='__all__'
        fields=['id','admin_id','admin','name','status','version','desc','create_time','update_time']

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Environment
        fields='__all__'