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

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        # fields='__all__'
        fields=['id','admin','name','status','version','desc']

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Environment
        fields='__all__'