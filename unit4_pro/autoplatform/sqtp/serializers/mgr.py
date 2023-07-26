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
    project_id=serializers.IntegerField(write_only=True)
    project=ProjectSerializer(read_only=True)
    category=serializers.SerializerMethodField()
    os=serializers.SerializerMethodField()
    status=serializers.SerializerMethodField()

    def get_status(self,obj):
        return obj.get_status_display()
    def get_os(self,obj):
        return obj.get_os_display()
    def get_category(self,obj):
        return obj.get_category_display()
    def validate_project_id(self, project_id):
        if not Project.objects.filter(pk=project_id).count():
            raise serializers.ValidationError('请传递正确的project_id')
        return project_id

    class Meta:
        model=Environment
        fields='__all__'